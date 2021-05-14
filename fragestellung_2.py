#### frage 2: Welcher Kontinent verzeichnet den grössten BIP-Zuwachs in der Periode von 2000-2019?
####
#### input: country_stage.csv, länderkode_stage.csv, rgdpna.csv
#### output:
#### method: verbinden von country_stage.csv mit rgdpna.csv via länderkürzel-ländername von länderkode_stage.csv
#### laypout df: kontinent, ländername, jahr, bip

#load libraries and set genreals
import warnings
warnings.filterwarnings('ignore')
from distutils.version import StrictVersion
import pandas as pd
assert StrictVersion(pd.__version__) >= StrictVersion('0.19.0')
import seaborn as sns
assert StrictVersion(sns.__version__) >= StrictVersion('0.7.0')

#load data
df_c = pd.read_csv('country_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('länderkode_stage.csv', header=0, encoding='utf-8')
df_r = pd.read_csv('rgdpna.csv', header=0, encoding='utf-8')


#first -> generals and irregularities inspection
df_c.head()
df_k.head()
df_r.head()
df_r.count()
df_r.info()

#drop superfluous column
df_r = df_r.drop(columns="VariableCode")

#join table together
df_joined_1 = pd.merge(df_c, df_k, on='Land', how='inner')
df_joined_1.head()
df_joined_1.info()
df_joined_2 = pd.merge(df_joined_1, df_r, left_on='ISO-3', right_on='RegionCode', how='inner')
df_joined_2.head()
df_joined_2.info()

#drop , resp. keep only row with year 2000 and 2019
df_j = df_joined_2.drop(df_joined_2[(df_joined_2.YearCode != 2000) & (df_joined_2.YearCode != 2019)].index)
df_j.head()
df_j.info()
df_j

#index the df
df_i = df_j.set_index(['Kontinent', 'YearCode'])

#group index with sum of column value
new_df = df_i.groupby(level= ['Kontinent', 'YearCode']).sum()

#reset the index to columns
df_res = new_df.reset_index()
df_res


df_res_2 = df_res.set_index(['Kontinent'])
df_res_2
#
for i in df_res["AggValue"]:
    x - i
    x = i