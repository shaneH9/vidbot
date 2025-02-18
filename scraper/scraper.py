import random
import requests
import re
from bs4 import BeautifulSoup
from urllib import request
import brotli
import gzip
import zlib

def newEggScrape():
    headers = {
        'Accept': 'text/html, image/avif, image/apng, image/svg+xml, */*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Site': 'none',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    searchTermWithSpaces = input("Select searchTerm: ")
    searchTerm = searchTermWithSpaces.replace(" ","+")
    url = f"https://www.newegg.com/p/pl?d={searchTerm}"

    resp = request.urlopen(request.Request(url, headers=headers))
    content_encoding = resp.getheader('Content-Encoding')
    data = resp.read()

    if content_encoding == 'br':
        data = brotli.decompress(data)
    elif content_encoding == 'gzip':
        data = gzip.decompress(data)
    elif content_encoding == 'deflate':
        data = zlib.decompress(data)

    content = data.decode('utf-8')
    parsedDoc = BeautifulSoup(content,"html.parser")
    maxPage = int(str(parsedDoc.find("span",class_="list-tool-pagination-text").strong).split("/")[-2].split(">")[-1][:-1])

    #traverse different pages 
    for page in range(1, maxPage+1):
        url = f"https://www.newegg.com/p/pl?d={searchTerm}&page={page}"
        resp = request.urlopen(request.Request(url, headers=headers))
        content_encoding = resp.getheader('Content-Encoding')
        data = resp.read()

        if content_encoding == 'br':
            data = brotli.decompress(data)
        elif content_encoding == 'gzip':
            data = gzip.decompress(data)
        elif content_encoding == 'deflate':
            data = zlib.decompress(data)

        content = data.decode('utf-8')
        parsedDoc = BeautifulSoup(content,"html.parser")
        neweggLogo = parsedDoc.find(class_="header2021-logo-img").find("img")['src']
        itemDiv = parsedDoc.find(class_="item-cells-wrap border-cells short-video-box items-list-view is-list")
        items = itemDiv.find_all(string = re.compile(searchTermWithSpaces))
        
        for item in items:
            if "Gaming PC" in item.string or "Gaming Desktop" in item.string:
                continue

            parent = item.parent
            if parent.name != "a":
                continue
            
            name = item
            link = parent['href']
            imageLink = item.find_parent().find_parent().find_parent().find(class_="item-img").find("img")['src']
            sale = False
            inStock = True
            discount = -1.0
            isRefurbished = ((parent.find(class_="item-open-box-italic").string) == "Refurbished ")
            priceWas = item.find_parent().find_parent().find_parent().find(class_="item-action").find(class_="price").find(class_="price-was").find(class_="price-was-data")
            stockGet = item.find_parent().find_parent().find_parent().find(class_="item-info").find(class_="item-promo")

            if stockGet is not None:
                inStock = False
            
            if priceWas is not None:
                sale = True
                priceWas = float(priceWas.string.replace("$","").replace(",",""))
                discount = ((priceWas-price) / price) *100

            try:
                price = int(item.find_parent().find_parent().find_parent().find(class_="item-action").find(class_="price-current").strong.string.replace(",",""))
                isComingSoon = False
            except:
                isComingSoon = True
                price = -1.0

            print(link)
            print(neweggLogo)
            print(imageLink)
            print(price)
            print(priceWas)
            print(sale)
            print(discount)
            print(item.string)
            print("coming soon: " + str(isComingSoon))
            print("in stock: " + str(inStock))
            print("refurbished? " + str(isRefurbished))
            #parse all info into a data structure
            print("============================================================")
