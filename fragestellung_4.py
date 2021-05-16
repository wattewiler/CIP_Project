#### frage 4: Gibt es eine statistisch feststellbare, signifikante Korrelation zwischen der Durchführung von...
####            Sportgrossanlässen und der Veränderung des BIPs der Gastgebernation?
####
#### input: 'c2_laendercode_stage.csv', 'a1_rgdpna_stage.csv'
#### output: plots
#### process: step 1: verbinden von 'a1_rgdpna_stage.csv' via länderkürzel-ländername von 'c2_laendercode_stage.csv'
####          step 2: auswahl von 4 ländern; 2 mit vielen sportgrossanlasereignissen, 2 mit niedrigem BIP
####          Step 3: time series analysis, detrending, ermittlung von outlier und anschliessender
####                  abgleich mit dem datum von sportevents im lande
#### target df layout: ländername, jahr, bip

#load libraries
import warnings
warnings.filterwarnings('ignore')
from distutils.version import StrictVersion
import pandas as pd
assert StrictVersion(pd.__version__) >= StrictVersion('0.19.0')
import seaborn as sns
assert StrictVersion(sns.__version__) >= StrictVersion('0.7.0')
#load libraries for time series analysis
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np


#load data
df_r = pd.read_csv('a1_rgdpna_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('c2_laendercode_stage.csv', header=0, encoding='utf-8')

#merge both data frames
df_j = pd.merge(df_r, df_k, left_on='RegionCode', right_on='ISO-3', how='inner')
df_j = df_j.drop(columns="ISO-3")
df_j = df_j.drop(columns="RegionCode")
df_j = df_j.drop(columns="VariableCode")

df_j.head()

#selection of country, from question 1: find top two countries:
df_c1 = df_j[df_j['Land'] == 'Frankreich']
df_c1.head()

#plot time series
df_c1.plot(x='YearCode', y='AggValue', marker='o', color='goldenrod', linewidth=3.0, figsize=(16,10))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of French GDP')

#detrending of time series
ts_detrended = signal.detrend(df_c1['AggValue'])
ts_detrended = signal.detrend(ts_detrended)

#plot detrended ts
plt.plot(df_c1['YearCode'], ts_detrended, label="GDP_detrended", color='lightsteelblue', linewidth=3.0, linestyle='dotted')
plt.title('Detrended Time Series of French GDP')







#### lessons learned
# -
