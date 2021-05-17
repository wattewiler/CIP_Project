#### webscrapping of data source C1; data dimansions: Country name, continent name
####
#### input: https://www.bernhard-gaul.de/wissen/staatenerde.php#uebneu
#### output: c1_country_src.csv

#   ladet die Libraries
import requests
from bs4 import BeautifulSoup as bs

#   download html file und unwanldung in soup objekt
raw_html = requests.get("https://www.bernhard-gaul.de/wissen/staatenerde.php#uebneu")
soup_html = bs(raw_html.text, "html.parser")

#   loop durch das html code und speichert die gesuchten, linie für linie.
csv_file = open("c1_country_src.csv", "w", encoding='utf-8')
for p in soup_html.select("tr"):
    y = p.select("td")
    a = y[0].text
    b = y[1].text
    csv_file.write(a + "," + b + "\n")
    print(a + ",")
csv_file.close()

#### Lessons learned:
#   - wie bei web_scrapper_b1 ist das webpage html einfach geholten und ohne grosse struktur. die kleine
#       auswahl von html tags und attributen machten es kaum möglich, einen html muster für die
#       extraktion zu erkennen.