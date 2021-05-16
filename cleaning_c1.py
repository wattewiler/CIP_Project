#### cleaning country_dirty.csv
####
#### input: country_dirty.csv
#### Output: country_stage.csv


#load libraries and set genreals
import pandas as pd


#load data - first probelm with unintended presence of 3rd column
#df = pd.read_csv('country_dirty.csv')

#thus, load wand set manually the header, skip first row
df = pd.read_csv('country_dirty.csv', header=None, skiprows=1, names=['Kontinent', 'Land'], encoding='utf-8')

#first data inspection
df.head()
df.describe()
df.info()

#first cleaning - get rid of undesired rows at the end
print(df.groupby('Kontinent').count())
df[-15:]

df.drop(df.loc[242:252].index, inplace=True)


#second - correct Null values
df[df['Kontinent'].isnull()]    #no null values in kontinent
df[df['Land'].isnull()]

df.loc[23]
df.loc[23] = ["Afrika", "Benin"]

df.loc[32]
df.loc[32] = ["Afrika", "Burkina Faso"]

df.loc[67]
df.loc[67] = ["Australien", "Guam"]

df.loc[80]
df.loc[80] = ["Europa", "Irland"]

df[df['Land'].isnull()]
df.loc[107]["Land"] = "Korea (Nord)"
df = df.drop([108])

# third - correct misspelling (Europe -> Europa)
print(df.groupby('Kontinent').count())
df[df['Kontinent'] == 'Europe']
df['Kontinent'][4] = 'Europa'
df['Kontinent'][81] = 'Europa'

# 4th - find lower case and change them with upper case
# lowercased.map() might had been easier
count = 1
for p in df["Land"]:
    if p[0].islower():
        df["Land"][count] = (p[0].upper() + df["Land"][count][1:])
        print(p)                    # to see what is wrong
        print(df["Land"][count])    # to see te correction
    count += 1

#save data frame into new csv file
df.to_csv(r'country_stage.csv', index = False, header=True)

### lessons learned
# - index, iloc, loc -> wenn nicht spezifiziert, erstellt ein pd dataframe eine liste "Index", beginnend mit 0.
#       Diese PD Data frame indexierung ist nicht das bekannte "index", sondern eben eine Liste.
#       Wird ein Zeile entfernt, führt das nicht zum nachrücken des DF Index Nummern und es enstehen Lücken in der Numerierung.
#       Dies kann gegebenfalls z.B. beim loopen zu Fehlern führen.