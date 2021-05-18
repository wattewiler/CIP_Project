#### frage 4: Gibt es eine statistisch feststellbare, signifikante Korrelation zwischen der Durchführung von...
####            Sportgrossanlässen und der Veränderung des BIPs der Gastgebernation?
####
#### input: 'c2_laendercode_stage_2.csv', 'a1_rgdpna_stage.csv'
#### output: plots
#### process: step 1: verbinden von 'a1_rgdpna_stage.csv' via länderkürzel-ländername von 'c2_laendercode_stage.csv'
####          step 2: auswahl aus fragestelung 1: die top vier event länder
####          Step 3: time series analysis, detrending, ermittlung von outlier und anschliessender
####                  abgleich mit dem datum von sportevents im lande


#   ladet die libraries
import pandas as pd
import seaborn as sns
#   ladet libraries für die time series analysis
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np


#   ladet die bereinigten csv
df_r = pd.read_csv('a1_rgdpna_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('c2_laendercode_stage_2.csv', header=0, encoding='utf-8')

#   verbindet beide datensets - über die iso-3 kennzeichnung wird das bip dem ganzen ländername zugewiesen
df_j = pd.merge(df_r, df_k, left_on='RegionCode', right_on='ISO-3', how='inner')
df_j.head()

#   beseitigt überflüssige spalten
df_j = df_j.drop(columns="ISO-3")
df_j = df_j.drop(columns="RegionCode")
df_j = df_j.drop(columns="VariableCode")

df_j.head()

#   auswahl der länder für die anaylse -> findings aus fragestellung_1:
#   1. usa 2. frankreich 3. italien 4. deutschland
df_usa = df_j[df_j['Land'] == 'USA']
df_fr = df_j[df_j['Land'] == 'Frankreich']
df_ita = df_j[df_j['Land'] == 'Italien']
df_de = df_j[df_j['Land'] == 'Deutschland']
df_usa.head()
df_fr.head()
df_ita.head()
df_de.head()

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
