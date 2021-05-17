#### cleaning c1_country_src_dirty.csv
####
#### input: c1_country_src_dirty.csv
#### Output: c1_country_stage.csv


#   ladet die Libraries
import pandas as pd


#   der erste versuch, das csv einzulesen schlug fehl. dies, weil der titel spezialzeichen enthält...
#df = pd.read_csv('c1_country_src_dirty.csv')

#   ... desswegen wird die titelzeile ausgelassen (skiprows) und der header wird manuel eingegeben
df = pd.read_csv('c1_country_src_dirty.csv', header=None, skiprows=1, names=['Kontinent', 'Land'], encoding='utf-8')

#   erste daten-inspektion
df.head()
df.describe()
df.info()

#   1. cleaning - ungewollte zeilen am ende des csv werden herausgeschnitten
print(df.groupby('Kontinent').count())
df[-15:]

df.drop(df.loc[242:252].index, inplace=True)


#   2. - findet null werte und behebt sie
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

#   3. - korrieigert falschschreibung (Europe -> Europa)
print(df.groupby('Kontinent').count())
df[df['Kontinent'] == 'Europe']
df['Kontinent'][4] = 'Europa'
df['Kontinent'][81] = 'Europa'

#   2. - findet falsche kleinschreibung und korrigiert sie
#       -> lowercased.map() wäre dafür villeicht schneller gewesen
count = 1
for p in df["Land"]:
    if p[0].islower():
        df["Land"][count] = (p[0].upper() + df["Land"][count][1:])
        print(p)                    # to see what is wrong
        print(df["Land"][count])    # to see te correction
    count += 1

#   speichert das dataframe in ein csv, ohne index und mit header
df.to_csv(r'c1_country_stage.csv', index = False, header=True)

### lessons learned
# - index, iloc, loc -> wenn nicht spezifiziert, erstellt ein pd dataframe eine liste "Index", beginnend mit 0.
#       Diese PD Data frame indexierung ist nicht das bekannte "index", sondern eben eine Liste.
#       Wird ein Zeile entfernt, führt das nicht zum nachrücken des DF Index Nummern und es enstehen Lücken in der Numerierung.
#       Dies kann gegebenfalls z.B. beim loopen zu Fehlern führen.