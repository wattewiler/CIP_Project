#### webscrapping of data source C1; data dimansions: Country name, continent name
####
#### input: https://www.bernhard-gaul.de/wissen/staatenerde.php#uebneu
#### output: country_cip.csv

#load libraries
import requests
from bs4 import BeautifulSoup as bs

#download html file and convert into soup object
raw_html = requests.get("https://www.bernhard-gaul.de/wissen/staatenerde.php#uebneu")
soup_html = bs(raw_html.text, "html.parser")

#load extracted text into csv file
csv_file = open("country_cip.csv", "w", encoding='utf-8')
for p in soup_html.select("tr"):
    y = p.select("td")
    a = y[0].text
    b = y[1].text
    csv_file.write(a + "," + b + "\n")
csv_file.close()