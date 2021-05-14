#### cleaning country_dirty.csv
####
#### input: country_dirty.csv
#### Output: country_stage.csv


#load libraries and set genreals
import warnings
warnings.filterwarnings('ignore')
from distutils.version import StrictVersion
import pandas as pd
assert StrictVersion(pd.__version__) >= StrictVersion('0.19.0')
import seaborn as sns
assert StrictVersion(sns.__version__) >= StrictVersion('0.7.0')

#load data - first probelm with unintended presence of 3rd column
#df = pd.read_csv('country_dirty.csv')

#thus, load wand set manually the header, skip first row
df = pd.read_csv('country_dirty.csv', header=None, skiprows=1, names=['Kontinent', 'Land'], encoding='utf-8')

#first -> generals and irregularities inspection
df.head()
df.describe()
df.info()

#first measurement - get rid of undesired rows at the end
print(df.groupby('Kontinent').count())
df[-15:]

df.drop(df.loc[242:252].index, inplace=True)


#correct or delete Null values
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

# correct misspelling (Europe -> Europa) !!! create error
print(df.groupby('Kontinent').count())
df[df['Kontinent'] == 'Europe']
df['Kontinent'][4] = 'Europa'
df['Kontinent'][81] = 'Europa'

#third - find lower case and change them with upper case
# lowercased.map() might had been easier
count = 1
for p in df["Land"]:
    if p[0].islower():
        df["Land"][count] = (p[0].upper() + df["Land"][count][1:])
        print(p)
        print(df["Land"][count])
    count += 1

#save data frame into new csv file
df.to_csv(r'country_stage.csv', index = False, header=True)

### lessons learned
### index, iloc, loc -> wenn nicht spezifiziert, erstellt ein pd dataframe eine liste "Index", beginnen mit 0.
# Zu beachten ist, dass diese "index"-liste nicht das uns bekannte index ist, sondern eben eine Liste.
# arbeitet mensch mit dieser liste und verwechselt diese mit dem Index, kann dies verwirrend wirken.
# Beispiel: im oberen Beispiel führte das Entfernen einer zeile nicht zu einem nachrücken der Index Liste,
# da diese eben eine Liste ist, und nicht das eigentliche index. D.h, die ""Index""- Werte des Pandas Dataframe,
# gespeichert als Liste und bennant als "Index", sind fest zugeordnet und rücken nicht nach.
# Lücken können enstehen und dies kann beim z.B. loopen zu Fehlern führen.
# erhält die Indexierung des pd df anderen Werte, e.g. Namen, würde solch ein Fehler schneller Bermerkbar werden.