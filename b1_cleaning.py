#### cleaning b1_wm_src_dirty.csv
####
#### input: b1_wm_src_dirty.csv.csv
#### output: b1_wm_stage.csv.csv


#   ladet die Libraries
import pandas as pd


#   ladet das csv und fügt einen titel hinzu
df = pd.read_csv('b1_wm_src_dirty.csv', header=None, names=['Land', 'Jahr'], encoding='utf-8')

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

#   1. cleaning - falschgelesen zeile wegen eines semicolon
print(df['Land'][14])
df['Land'][14] = "USA"
df['Jahr'][14] = "1994"
df.count()

#   2. - findet falsche kleinschreibung und korrigiert sie
#       -> lowercased.map() wäre dafür villeicht schneller gewesen
count = 0
for p in df["Land"]:
    if df["Land"][count][0].islower():
        print(p)
        df["Land"][count] = (df["Land"][count][0].upper() + df["Land"][count][1:])
    count += 1

print(df)

#   3. - korrigiert falsche datumformaten
count = 0
for p in df["Jahr"]:
    if len(df["Jahr"][count]) > 4:
        print(p)
        df["Jahr"][count] = df["Jahr"][count][-4:]
    count += 1

print(df["Jahr"])

#   letzter check
df.info()

#   speichert die daten in ein csv file, ohne index und mit header
df.to_csv(r'b1_wm_stage.csv', index = False, header=True)