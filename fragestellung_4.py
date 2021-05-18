#### frage 4: Gibt es eine statistisch feststellbare, signifikante Korrelation zwischen der Durchführung von...
####            Sportgrossanlässen und der Veränderung des BIPs der Gastgebernation?
####
#### input: 'c2_laendercode_stage_2.csv', 'a1_rgdpna_stage.csv'
#### output: plots
#### process: step 1: verbinden der datensets: 'a1_rgdpna_stage.csv' und 'c2_laendercode_stage.csv'
####          step 2: auswahl der länder aus fragestelung 1: die top vier länder
####          Step 3: time series analysis: detrending, regressionslinie, hervorbringen von events


#   ladet die libraries
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import xlsxwriter


#   ladet die bereinigten csv
df_r = pd.read_csv('a1_rgdpna_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('c2_laendercode_stage_v2.csv', header=0, encoding='utf-8')

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
df_it = df_j[df_j['Land'] == 'Italien']
df_de = df_j[df_j['Land'] == 'Deutschland']
df_usa.head()
df_fr.head()
df_it.head()
df_de.head()

#   erstellt ein plot von den bip über die zeit pro land
#   anschliessend wird der plot als png abgespeichert, für später zum excel file
df_usa.plot(x='YearCode', y='AggValue', marker='o', color='goldenrod', linewidth=2.0, figsize=(16,10))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of US GDP')
plt.savefig('fragestellung_4_usa_bip_time_series')

df_fr.plot(x='YearCode', y='AggValue', marker='o', color='steelblue', linewidth=2.0, figsize=(16,10))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of french GDP')
plt.savefig('fragestellung_4_frankreich_bip_time_series')

df_it.plot(x='YearCode', y='AggValue', marker='o', color='yellowgreen', linewidth=2.0, figsize=(16,10))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of italian GDP')
plt.savefig('fragestellung_4_italien_bip_time_series')

df_de.plot(x='YearCode', y='AggValue', marker='o', color='dimgray', linewidth=2.0, figsize=(16,10))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of german GDP')
plt.savefig('fragestellung_4_deutschland_bip_time_series')

#   entrendet die time series
usa_detrended = signal.detrend(df_usa['AggValue'])
fr_detrended = signal.detrend(df_fr['AggValue'])
it_detrended = signal.detrend(df_it['AggValue'])
de_detrended = signal.detrend(df_de['AggValue'])

#plot detrended ts
plt.plot(df_usa['YearCode'], ts_detrended, label="GDP_detrended", color='navajowhite', linewidth=3.0, linestyle='dotted')
x = []
y = []
plt.plot(x, y, "or")
plt.title('Detrended Time Series of US GDP')
plt.savefig('fragestellung_4_usa_time_series_analyse')

plt.plot(df_fr['YearCode'], ts_detrended, label="GDP_detrended", color='lightsteelblue', linewidth=3.0, linestyle='dotted')
x = []
y = []
plt.plot(x, y, "or")
plt.title('Detrended Time Series of french GDP')
plt.savefig('fragestellung_4_fr_time_series_analyse')

plt.plot(df_it['YearCode'], ts_detrended, label="GDP_detrended", color='darkseagreen', linewidth=3.0, linestyle='dotted')
x = []
y = []
plt.plot(x, y, "or")
plt.title('Detrended Time Series of italian GDP')
plt.savefig('fragestellung_4_it_time_series_analyse')

plt.plot(df_de['YearCode'], ts_detrended, label="GDP_detrended", color='slategray', linewidth=3.0, linestyle='dotted')
x = []
y = []
plt.plot(x, y, "or")
plt.title('Detrended Time Series of german GDP')
plt.savefig('fragestellung_4_de_time_series_analyse')

#   fügt die plots png in ein excel sheet ein
workbook = xlsxwriter.Workbook('Result_Question_04.xlsx')
worksheet = workbook.add_worksheet("usa")
worksheet.insert_image('B2', 'fragestellung_4_usa_bip_time_series.png')
worksheet.insert_image('L2', 'fragestellung_4_usa_time_series_analyse.png')

worksheet = workbook.add_worksheet("fr")
worksheet.insert_image('B2', 'fragestellung_4_frankreich_bip_time_series.png')
worksheet.insert_image('L2', 'fragestellung_4_fr_time_series_analyse.png')

worksheet = workbook.add_worksheet("it")
worksheet.insert_image('B2', 'fragestellung_4_italien_bip_time_series.png')
worksheet.insert_image('L2', 'fragestellung_4_it_time_series_analyse.png')

worksheet = workbook.add_worksheet("de")
worksheet.insert_image('B2', 'fragestellung_4_deutschland_bip_time_series.png')
worksheet.insert_image('L2', 'fragestellung_4_de_time_series_analyse.png')

workbook.close()


#### lessons learned
# -
