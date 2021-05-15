#### cleaning wm_dirty.csv
####
#### input: wm_dirty.csv.csv
#### output: wm_stage.csv.csv


#load libraries and set genreals
import pandas as pd


#load data
df = pd.read_csv('wm_dirty.csv', header=None, names=['Land', 'Jahr'], encoding='utf-8' )

#first -> general and irregularities inspection
df.head()
df.count()
df.info()
df.isnull()

#convert any ä, ü and ö into ae, ue and oe - for unification purposes with c1
df = df.replace('ä', 'ae', regex=True)
df = df.replace('ö', 'oe', regex=True)
df = df.replace('ü', 'ue', regex=True)
df = df.replace('Ä', 'Ae', regex=True)
df = df.replace('Ö', 'Oe', regex=True)
df = df.replace('Ü', 'Ue', regex=True)
df

#first cleaning
print(df['Land'][14])
df['Land'][14] = "USA"
df['Jahr'][14] = "1994"
df.count()

#second - search for duplicates
df.duplicated()         #no duplicates!

#third - find lower case and change them with upper case
# lowercased.map() might had been easier
count = 0
for p in df["Land"]:
    if df["Land"][count][0].islower():
        print(p)
        df["Land"][count] = (df["Land"][count][0].upper() + df["Land"][count][1:])
    count += 1

print(df["Land"])

#4th overall inspection
df

#4th - correct wrong date entry
count = 0
for p in df["Jahr"]:
    if len(df["Jahr"][count]) > 4:
        print(p)
        df["Jahr"][count] = df["Jahr"][count][-4:]
    count += 1

print(df["Jahr"])

#last check
df.info()

#save data frame into new csv file
df.to_csv(r'wm_stage.csv', index = False, header=True)