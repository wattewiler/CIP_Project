#### cleaning ländercode.csv
####
#### input: länderkode.csv
#### output: länderkode_stage.csv


#load libraries and set genreals
import warnings
warnings.filterwarnings('ignore')
from distutils.version import StrictVersion
import pandas as pd
assert StrictVersion(pd.__version__) >= StrictVersion('0.19.0')
import seaborn as sns
assert StrictVersion(sns.__version__) >= StrictVersion('0.7.0')

#load data
df = pd.read_csv('länderkode.csv', header=0, sep='\t', encoding='utf-8')

#first -> generals and irregularities inspection
df.head()
df.count()
df.info()

#convert any ä, ü and ö into ae, ue and oe - for unification purposes with c1
df = df.replace('ä', 'ae', regex=True)
df = df.replace('ö', 'oe', regex=True)
df = df.replace('ü', 'ue', regex=True)
df

#drop superfluous column
df = df.drop(columns="ISO-2")
df = df.drop(columns="numerisch")

#save data frame into new csv file
df.to_csv(r'länderkode_stage.csv', index = False, header=True)