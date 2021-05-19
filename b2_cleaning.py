# Erst erfolgt der Import der benötigten Libraries
import pandas as pd

# Danach wird das CSV eingelesen und der Outputname des CSV definiert
df = pd.read_csv('b2_wolympics_src.csv', encoding='utf-8')
csv_output_name = 'b2_wolympics_stage.csv'

# Hier verschaffen wir uns einen Überblick der eingelesenen Daten
df.info()

# Eingehender Check der Daten (bei einem kleinen Dataframe kein Problem)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# Alle Zeilen, die komplett leer sind (NaN, also keine Values haben), werden jetzt gedroppt
df = df.dropna(how='all')

# Alle Kolonnen, die nicht gebraucht werden, werden ebenso gedroppt
to_drop = ['Teilnehmer',
           'Wettbewerbe',
           'Beste Nationen',
           'BesteÂ Sportler']

df.drop(to_drop, inplace=True, axis=1)

# Jahrzahlen in neue Kolonne 'Jahr_stage' extrahieren, alle Whitespaces löschen und Datatype INT setzen
df['Jahr_stage'] = df['Jahr'].str[:4]
df['Jahr_stage'] = df['Jahr_stage'].str.replace(' ', '')
df['Jahr_stage'] = df['Jahr_stage'].astype('int64')

# Umbenennen der Kolonne, in welcher die Spiele stattgefunden haben
df.rename(columns={'Olympische Winterspiele in': 'Land'}, inplace=True)

# Länderkürzel in neue Kolonne 'Land_code' extrahieren
df['Land_code'] = df['Land'].str.replace(r'[^(]*\(|\)[^)]*', '')

# Länderkürzel in neuer Kolonne 'Land_code_stage' durch ISO3-Norm-Values ersetzen
df['Land_code_stage'] = df['Land_code'].replace(['F', 'CH', 'D', 'JAP', 'IT', 'JP', 'JUG', 'SÃ¼dkorea'],
                                                ['FRA', 'CHE', 'DEU', 'JPN', 'ITA', 'JPN', 'BIH', 'KOR'])

# Der Vollständigkeit halber eine weitere Spalte zur Deklaration des Anlasses
df['Anlass_stage'] = 'Olympische Winterspiele'

# Abschliessend nochmals ein kurzer Check, ob das Dataframe sauber aufbereitet ist. Dafür werden die Kolonnen ausgegeben
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# Alle Kolonnen, die nach dem Cleaning nicht mehr gebraucht werden, werden vor Output gedroppt
to_drop = ['Jahr',
           'Land',
           'Land_code', ]

df.drop(to_drop, inplace=True, axis=1)

# Umbenennung der sauberen, korrekten Spalten zur Ausgabe
df['Land_code'] = df['Land_code_stage']
df['Jahr'] = df['Jahr_stage']
df['Anlass'] = df['Anlass_stage']

# Schlussendlich werden die Daten in ein neues CSV-File geschrieben, der Index dabei entfernt, der Header belassen
df[['Jahr', 'Land_code', 'Anlass']].to_csv(csv_output_name, index=False, header=True)

#### LESSONS LEARNED ####
# Bei der Aufbereitung von gescrapten Daten ist es eminent wichtig, dass die Originalinformationen beibehalten werden.
# Das bedeutet also, dass vor einer Manipulation am Dataframe eine exakte Kopie der betroffenen Spalte/Zeile erstellt
# wird. Einige Male war ich mir nicht mehr ganz sicher, an welcher Kolonne ich die Manipulation vorgenommen hatte oder
# droppte Daten, die ich eigentlich noch gebraucht hätte. Deshalb muss ein Naming-Scheme entwickelt und innerhalb des
# Teams angewendet und eingalten werden. Dabei haben sich die Tipps der Dozenten als sehr wertvoll erwiesen.