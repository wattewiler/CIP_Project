#### cleaning ländercode.csv
####
#### input: länderkode.csv
#### output: länderkode_stage.csv


#load libraries and set genreals
import pandas as pd


#load data
df = pd.read_csv('länderkode.csv', header=0, sep='\t', encoding='utf-8')

#first general data inspection
df.head()
df.count()
df.info()

#convert any ä, ü and ö into ae, ue and oe - for unification purposes with c1
df = df.replace('ä', 'ae', regex=True)
df = df.replace('ö', 'oe', regex=True)
df = df.replace('ü', 'ue', regex=True)
df = df.replace('Ä', 'Ae', regex=True)
df = df.replace('Ö', 'Oe', regex=True)
df = df.replace('Ü', 'Ue', regex=True)
df

#drop superfluous column
df = df.drop(columns="ISO-2")
df = df.drop(columns="numerisch")

#save data frame into new csv file
df.to_csv(r'länderkode_stage.csv', index = False, header=True)