import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.taschenhirn.de/sport/olympische-sommerspiele/"
csv_output_name = "summer_olympics.csv"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
#print(soup.prettify()) # print the parsed data of html

summer_olympics_table = soup.find("table", attrs={"class": "dataList"})
summer_olympics_table_data = summer_olympics_table.tbody.find_all("tr")

headers = []
for i in summer_olympics_table.find_all('th'):
    title = i.text.strip()
    headers.append(title)

rows = []
for row in summer_olympics_table_data:
    value = row.find_all('td')
    beautified_value = [ele.text.strip() for ele in value]
    # Remove data arrays that are empty
    if len(beautified_value) == 0:
        continue
    rows.append(beautified_value)

with open(csv_output_name, 'w', newline="") as output:
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)