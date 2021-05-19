# Zuerst werden die benötigten Libraries importiert
import requests
from bs4 import BeautifulSoup
import csv

# Hier sind In- und Output definiert. Als Input die URL, die gescraped wird, und als Output der CSV-Filename des Exports
url = "https://www.taschenhirn.de/sport/olympische-winterspiele/"
csv_output_name = "b2_wolympics_src.csv"

# Mit einem Get-Request werden die rohen HTML-Daten geladen...
html_content = requests.get(url).text

# ...und mittels LXML geparsed
soup = BeautifulSoup(html_content, "lxml")

# Ein erstes Print des gescrapten HTML-Inhalts gibt uns eine Übersicht der geladenen Daten
print(soup.prettify())

# Als -olympics_table wird der Inhalt des Tags <table> mit der Klasse "dataList" geladen
# Danach wird -olympics_table nach allen Tags <tr> durchsucht
winter_olympics_table = soup.find("table", attrs={"class": "dataList"})
winter_olympics_table_data = winter_olympics_table.tbody.find_all("tr")

# Damit die Daten bzw. Kolonnen auch benennt werden, scrapen wir hier die Überschriften der Tabelle
headers = []
for i in winter_olympics_table.find_all('th'):
    title = i.text.strip()
    headers.append(title)

# Wir lassen uns die geladenen Überschriften ausgeben
print(headers)

# In _olympics_table_data werden nun alle Tags <td> gesucht und in rows[] gespeichert.
# Diese Tags beinhalten pro Datensatz einen Wert (Jahr, Ort etc.)
rows = []
for row in winter_olympics_table_data:
    value = row.find_all('td')
    beautified_value = [ele.text.strip() for ele in value]
# Data Arrays werden entfernt, falls sie leer sind
    if len(beautified_value) == 0:
        continue
    rows.append(beautified_value)

# Die Kolonnen werden zur Kontrolle ausgegeben
print(rows)

# Schlussendlich wird unter dem eingangs definitierten Namen eine CSV-Datei exportiert und kann im nächsten Schritt
# (Cleaning) weiterverarbeitet werden
with open(csv_output_name, 'w', newline="") as output:
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)

#### LESSONS LEARNED ####
# BeautifulSoup ist ein mächtiges Werkzeug und erlaubt es mit wenig aufwand, elegant Webseiten zu scrapen.
# Wichtig ist es, dass man sich zuerst eine gute Übersicht über die Webseite verschafft - schliesslich muss man
# wissen, mit was man da arbeitet. Dafür ist ein gewisses HTML- und CSS-Verständnis notwendig, welches ich auch gleich
# etwas vertiefen konnte. (Tatsächlich hat mir ein Missverständnis des Table-Tags einige Stunden Mehraufwand beschert...
# Ein Fehler, der mir bestimmt nicht mehr passieren wird!) Schlussendlich gibt es verschiedene Herangehensweisen,
# die zum selben Ziel führen. Es ist Webseite-abhängig, welche Methode sich wofür am besten eignet.