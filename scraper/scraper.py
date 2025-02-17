import random
import requests
import re
from bs4 import BeautifulSoup
from urllib import request
import brotli

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
searchTerm = input("Select searchTerm: ").replace(" ","+")
print(searchTerm)
url = f"https://www.newegg.com/p/pl?d={searchTerm}"


resp = request.urlopen(request.Request(url, headers=headers))
content_encoding = resp.getheader('Content-Encoding')
data = resp.read()

if content_encoding == 'br':
    data = brotli.decompress(data)
content = data.decode('utf-8')
parsedDoc = BeautifulSoup(content,"html.parser")
maxPage = int(str(parsedDoc.find("span",class_="list-tool-pagination-text").strong).split("/")[-2].split(">")[-1][:-1])


for page in range(1, maxPage+1):
    url = f"https://www.newegg.com/p/pl?d={searchTerm}&page={page}"
    resp = request.urlopen(request.Request(url, headers=headers))
    content_encoding = resp.getheader('Content-Encoding')
    data = resp.read()

    if content_encoding == 'br':
        data = brotli.decompress(data)
    content = data.decode('utf-8')
    parsedDoc = BeautifulSoup(content,"html.parser")

    itemDiv = parsedDoc.find(class_="item-cells-wrap border-cells short-video-box items-list-view is-list")
    items = itemDiv.find_all(text = re.compile(searchTerm))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent['href']
        print(link)