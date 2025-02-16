import requests
import re
from bs4 import BeautifulSoup

def checkBBstock():
    url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-5070-12gb-gddr7-graphics-card-graphite-grey/6614154.p?skuId=6614154"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
    }
    bestBuyResult = requests.get(url, headers=headers)

    bestBuy = BeautifulSoup(bestBuyResult.text, "html.parser")
    button = bestBuy.find("button", class_='add-to-cart-button')
    return button.get('data-button-state') != 'COMING_SOON'

