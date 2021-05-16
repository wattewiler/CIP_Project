#### webscrapping of data source B1; data dimensions: Country name, year
####
#### input: https://www.fussball-wm-total.de/History/histehre.html
#### output: b1_wm_src.csv

#load libraries
import requests
from bs4 import BeautifulSoup as bs

#download html file and convert into soup object
raw_html = requests.get("https://www.fussball-wm-total.de/History/histehre.html")
soup_html = bs(raw_html.text, "html.parser")

#get most distinctive html structure to target input
extract = soup_html.find("table", width="430", border="1", cellpadding="10")

#loop through html lines, eliminate unwanted input values and store as csv
csv_file = open("b1_wm_src.csv", "w", encoding='utf-8')
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

#### Lessons learned:
# - "try-exept" became especially handy to find predefined data structure get rid of the rest. In this case,
#       it acts as an error and selection handling in one.
# - Some webpages are badly structured. They use just a few tags and attributes for everything and it is difficult
#       to recognize patterns for the code scrapping.