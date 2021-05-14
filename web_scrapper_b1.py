#### webscrapping of data source B1; data dimensions: Country name, year
####
#### input: https://www.fussball-wm-total.de/History/histehre.html
#### output: wm_cip.csv

#load libraries
import requests
from bs4 import BeautifulSoup as bs

#download html file and convert into soup object
raw_html = requests.get("https://www.fussball-wm-total.de/History/histehre.html")
soup_html = bs(raw_html.text, "html.parser")

#get nearest, distinctive html section to target input
extract = soup_html.find("table", width="430", border="1", cellpadding="10")

#loop through html section and eliminate unwanted input values
csv_file = open("wm_cip.csv", "w", encoding='utf-8')
for p in extract.select("tr"):
    y = p.select("td")
    try:
        a = y[0].text
        b = y[1].text
        csv_file.write(a + "," + b + "\n")
        print(a + "," + b + "\n")
    except:
        1
csv_file.close()
