# Erst erfolgt der Import der benötigten Libraries
import pandas as pd

# Danach wird das CSV eingelesen und der Outputname des CSV definiert
df = pd.read_csv('b3_solympics_src.csv', encoding='utf-8')
csv_output_name = 'b3_solympics_stage.csv'

# Überblick der eingelesenen Daten
df.info()

# Eingehender Check der Daten (bei einem kleinen Dataframe kein Problem)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# Alle Zeilen, die komplett leer sind (NaN, also keine Values haben), werden gedroppt
df = df.dropna(how='all')

# Alle Kolonnen, die nicht gebraucht werden, werden gedroppt
to_drop = ['Athleten',
           'Wettbewerbe',
           'Besonderheiten',
           'Seltene Sportarten']

df.drop(to_drop, inplace=True, axis=1)

# Zeile 14 wird dupliziert, da die Olympiade in diesem Jahr in zwei Ländern stattgefunden hatte
# Danach Index +1 und neu sortieren
df.loc[15] = ['1940 # XII', 'FIN']
df.index = df.index + 1
df = df.sort_index()

print(df)

# Jahrzahlen in neue Kolonne 'Jahr_stage' extrahieren, alle Whitespaces löschen und Datatype INT setzen
df['Jahr_stage'] = df['Olympiade'].str[:4]
df['Jahr_stage'] = df['Jahr_stage'].str.replace(' ', '')
df['Jahr_stage'] = df['Jahr_stage'].astype('int64')




# Umbenennen der Kolonne, in welcher die Spiele stattgefunden haben
df.rename(columns={'in': 'Land'}, inplace=True)

# Länderkürzel in neue Kolonne 'Land_code' extrahieren
df['Land_code'] = df['Land'].str.replace(r'[^(]*\(|\)[^)]*', '')



# Länderkürzel in neuer Kolonne 'Land_code_stage' durch ISO3-Norm-Values ersetzen
df['Land_code_stage'] = df['Land_code'].replace(['GR', 'F', 'GB', 'Berlin', 'B', 'NL', 'Deutsches Reich',
                                                 'Helsinki, Tokio', 'London', 'IT', 'JP', 'Mex',
                                                 'BRD', 'UdSSR', 'SÃ¼dkorea', 'E', 'BR'],
                                                ['GRC', 'FRA', 'GBR', 'DEU', 'BEL', 'NLD', 'DEU',
                                                 'JPN', 'GBR', 'ITA', 'JPN', 'MEX',
                                                 'DEU', 'RUS', 'KOR', 'ESP', 'BRA'])

# Der Vollständigkeit halber eine weitere Spalte zur Deklaration des Anlasses
df['Anlass_stage'] = 'Olympische Sommerspiele'

# Abschliessend nochmals ein kurzer Check, ob das Dataframe sauber aufbereitet ist. Dafür werden alle Kolonnen ausgegeben
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

df.info()


# Alle Kolonnen, die nach dem Cleaning nicht mehr gebraucht werden, werden vor Output gedroppt
to_drop = ['Olympiade',
           'Land',
           'Land_code']

df.drop(to_drop, inplace=True, axis=1)

# Umbenennung der sauberen, korrekten Spalten zur Ausgabe
df['Land_code'] = df['Land_code_stage']
df['Jahr'] = df['Jahr_stage']
df['Anlass'] = df['Anlass_stage']

# Schlussendlich werden die Daten in ein neues CSV-File geschrieben, der Index dabei entfernt, der Header belassen
df[['Jahr', 'Land_code', 'Anlass']].to_csv(csv_output_name, index = False, header=True)



####### LESSONS LEARNED #######
# ASDFASDFASDF

df.info()