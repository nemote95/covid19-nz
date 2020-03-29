import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

url = 'https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-cases'

response = requests.get(url)

soup = BeautifulSoup(response.text,  "html.parser")


f = open("covid19-nz.csv","a+")


numbers =""
lis = soup.find_all("td")[1:3]
for i in lis :
    numbers+= ","+ i.text

date = soup.find_all("p",class_="georgia-italic")[0].text.split(",")[1].strip(".")

f.write(date+numbers+"\n")
f.close()

