#### webscrapping of data source B1; data dimensions: Country name, year
####
#### input: https://www.fussball-wm-total.de/History/histehre.html
#### output: b1_wm_src.csv

#   ladet die Libraries
import requests
from bs4 import BeautifulSoup as bs

#   download html file und unwanldung in soup objekt
raw_html = requests.get("https://www.fussball-wm-total.de/History/histehre.html")
soup_html = bs(raw_html.text, "html.parser")

#   entnimmt aus dem html file der gewünschte absatz
extract = soup_html.find("table", width="430", border="1", cellpadding="10")

#   loop durch das html code, lässt ungewollte zeilen aus und speichert die gesuchten, linie für linie.
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

####    Lessons learned:
# - "try-exept" war besonders nützlich um nach einer struktur im html code zu suchen und den rest auszulassen.
#       zeilen die nicht der struktur entsprachen und so nicht zu den gesuchten elementen gehörten, aber nicht vorher
#       enfernt werden konnten, werden dabei einfach ausgelassen,
# - die ist etwas sonderbar formatiert und enthält keine repetitive structur. dies machte es kaum möglich,
#       einen html muster zu erkennen und danach zu filtern. das try-exept war dafür eine gute notlösung