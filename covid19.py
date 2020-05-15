import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


#sending request to the webpage
url = 'https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-cases'

response = requests.get(url)

soup = BeautifulSoup(response.text,  "html.parser")

#getting numbers and the report date using beautifulsoup
tds = soup.find_all("td")

today_cases = tds[1].text
total_cases = tds[0].text

report_date = soup.find_all("p",class_="georgia-italic")[0].text.split(",")[1].strip(".")
report_date = datetime.strptime(report_date.lstrip(), '%d %B %Y')

#creating a new record for the new report

new_report = {"Date":datetime.strftime(report_date,"%d/%m/%Y"), "Total":total_cases, "Last24":today_cases}

#save the new report
df_file_name = "covid19-nz.csv"
df = pd.read_csv(df_file_name)
print(new_report)
#to avoid repeating reports
if new_report["Date"] not in df["Date"].values:
    df = df.append([new_report])
    df.Date = df["Date"]
    df.to_csv(df_file_name, index=False)


#update regression
from sklearn.linear_model import LinearRegression
X = df.index.values.reshape(-1,1)
y = df['Last24']

print(X.shape,y.shape)
regr = LinearRegression()
model = regr.fit(X , y)


#visualization
import matplotlib.pyplot as plt

predicted_y = regr.predict(X)

plt.scatter(df['Date'].astype(str), y,  color='black')
plt.plot(df['Date'].astype(str), predicted_y, color='blue', linewidth=3)

plt.xlabel("Date")
plt.ylabel("Daily new cases")


plt.show()

