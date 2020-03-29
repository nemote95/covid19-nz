import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

#sending request to the webpage
url = 'https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-cases'

response = requests.get(url)

soup = BeautifulSoup(response.text,  "html.parser")

#getting numbers and the report date using beautifulsoup
tds = soup.find_all("td")

today_cases = tds[2].text
total_cases = tds[1].text

report_date = soup.find_all("p",class_="georgia-italic")[0].text.split(",")[1].strip(".")

#creating a new record for the new report
new_report = {"Date":report_date, "Total":total_cases, "Last24":today_cases}

#save the new report
df_file_name = "covid19-nz.csv"
df = pd.read_csv(df_file_name)

#to avoid repeating reports
if report_date not in df.Date.values:
    df = df.append([new_report])
    df.to_csv(df_file_name, index=False)

