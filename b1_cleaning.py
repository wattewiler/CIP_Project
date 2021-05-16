#### cleaning b1_wm_src_dirty.csv
####
#### input: b1_wm_src_dirty.csv.csv
#### output: b1_wm_stage.csv.csv


#load libraries
import pandas as pd


#load data
df = pd.read_csv('b1_wm_src_dirty.csv', header=None, names=['Land', 'Jahr'], encoding='utf-8')

#first data inspection
df.head()
df.count()
df.info()

#convert any ä, ü and ö into ae, ue and oe - for unification purposes with "c1" data
df = df.replace('ä', 'ae', regex=True)
df = df.replace('ö', 'oe', regex=True)
df = df.replace('ü', 'ue', regex=True)
df = df.replace('Ä', 'Ae', regex=True)
df = df.replace('Ö', 'Oe', regex=True)
df = df.replace('Ü', 'Ue', regex=True)
df

#first cleaning - correct clumn of a misread row
print(df['Land'][14])
df['Land'][14] = "USA"
df['Jahr'][14] = "1994"
df.count()

#second - search for duplicates
df.duplicated()         #no duplicates!

#third - find lower case and change them with upper case
# -> lowercased.map() might had been faster to code
count = 0
for p in df["Land"]:
    if df["Land"][count][0].islower():
        print(p)
        df["Land"][count] = (df["Land"][count][0].upper() + df["Land"][count][1:])
    count += 1

print(df)

#4th - correct wrong date entries
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
df.to_csv(r'b1_wm_stage.csv', index = False, header=True)