#### cleaning ländercode.csv
####
#### input: c2_laendercode_src.csv
#### output: c2_laendercode_stage.csv


#   ladet die Libraries
import pandas as pd


#   ladet das csv mit titel, erstellt die tabellen mittels \t
df = pd.read_csv('c2_laendercode_src.csv', header=0, sep='\t', encoding='utf-8')

#   erste daten-inspektion
df.head()
df.count()
df.info()

#   wandelt alle ä, ü, ö in ae, ue, oe - damit die namen file übergreifend konsistent sind
df = df.replace('ä', 'ae', regex=True)
df = df.replace('ö', 'oe', regex=True)
df = df.replace('ü', 'ue', regex=True)
df = df.replace('Ä', 'Ae', regex=True)
df = df.replace('Ö', 'Oe', regex=True)
df = df.replace('Ü', 'Ue', regex=True)
df

#   entfernt unnötige spalten
df = df.drop(columns="ISO-2")
df = df.drop(columns="numerisch")

#   speichert das dataframe in ein csv, ohne index und mit header
df.to_csv(r'c2_laendercode_stage.csv', index = False, header=True)