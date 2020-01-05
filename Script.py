import requests
from bs4 import BeautifulSoup
def get_urls_from_file(filename):
    URLs=open(filename).readlines()
    return URLs
def check_price(URLs):
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    for URL in URLs:
        page = requests.get(URL,headers=headers)
        htmlcontent=BeautifulSoup(page.content,'html.parser')
        title=str(htmlcontent.find("div", {"class": "small-12 columns product-title"})).splitlines()[1]
        price=str(htmlcontent.find("h3", {"class": "price is sk-clr1"})).splitlines()[2].strip()
        price=int(price.split('.',1)[0])
        print(title,price)
check_price(get_urls_from_file("URLs.txt"))