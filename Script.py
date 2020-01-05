import requests
from bs4 import BeautifulSoup
import smtplib
import time
def get_urls_from_file(filename):#takes file and return list of pair < URL , price i want to check > 
    url_price_list=[]
    file=open(filename,"r")
    for line in file.readlines():
        pair=line.strip().split(',')
        url_price_list.append((pair[0],pair[1]))
    return url_price_list

def check_price(url_price_list):
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    for pair in url_price_list:#i want to check for every url if the price is less than or equal the desired one
        page = requests.get(pair[0],headers=headers)
        htmlcontent=BeautifulSoup(page.content,'html.parser')
        title=str(htmlcontent.find("div", {"class": "small-12 columns product-title"})).splitlines()[1].replace('<h1>','').replace('</h1>','')#parcing stuff to get the title
        price=str(htmlcontent.find("h3", {"class": "price is sk-clr1"})).splitlines()[2].strip()#same but to the price
        price=int(price.split('.',1)[0].replace(',',''))
        desired_price=int(pair[1])
        if price<=desired_price:
            send_mail(title,pair)     

def send_mail(title,pair):
    server=smtplib.SMTP('smtp.gmail.com',587)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('youremail@gmail.com','yourpassword')
        subject = 'THE PRICE OF THIS ITEM FELL DOWN!!'
        body = ' Hello, The price of '+ title + ' HAS FELL DOWN GO PURSHACE IT NOW ' + pair[0]
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            'youremail@gmail.com',
            'toemail@gmail.com',
            msg
        )
        print('EMAIL SENT!')
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 
    
while True:
    check_price(get_urls_from_file("URLs.txt"))
    time.sleep(30*60) #run the script every 30 mins