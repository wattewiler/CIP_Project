# Erst erfolgt der Import der benötigten Libraries
import pandas as pd

# Danach wird das CSV eingelesen und der Outputname des CSV definiert
df = pd.read_csv('b2_wolympics_src.csv', encoding='utf-8')
csv_output_name = 'b2_wolympics_stage.csv'

# Inspektion der eingelesenen Daten
df.info()

# Alle Zeilen, die komplett leer sind (NaN, also keine Values haben), werden gedroppt
df = df.dropna(how='all')

# Alle Kolonnen, die nicht gebraucht werden, werden gedroppt
to_drop = ['Teilnehmer',
           'Wettbewerbe',
           'Beste Nationen',
           'BesteÂ Sportler']
df.drop(to_drop, inplace=True, axis=1)

# Genaue Jahrzahlen in neue Kolonne 'Jahr_stage' extrahieren, alle Whitespaces löschen und Datatype INT setzen
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
# Weitere Spalte zur Deklaration des Anlasses
df['Anlass_stage'] = 'Olympische Winterspiele'

# Abschliessend ein kurzer Check, ob das Dataframe sauber aufbereitet ist. Dafür werden alle Kolonnen ausgegeben
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

df.info()

# Schlussendlich werden die Daten in ein neues CSV-File geschrieben
df['Jahr_stage', 'Land_code_stage', 'Anlass_stage'].to_csv(csv_output_name, index = False, header=True)