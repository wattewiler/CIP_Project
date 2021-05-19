#### frage 4: Gibt es eine statistisch feststellbare, signifikante Korrelation zwischen der Durchführung von...
####            Sportgrossanlässen und der Veränderung des BIPs der Gastgebernation?
####
#### input: 'c2_laendercode_stage_2.csv', 'a1_rgdpna_stage.csv', 'fragestellung_4_top4_laender.csv'
#### output: plots
#### process: step 1: verbinden der datensets: 'a1_rgdpna_stage.csv' und 'c2_laendercode_stage.csv'
####          step 2: auswahl der länder aus fragestelung 1: die top vier länder
####          Step 3: time series analysis: detrending, regressionslinie, hervorbringen von events


#   ladet die libraries
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal
import xlsxwriter
import pylab


#   ladet die bereinigten csv
df_r = pd.read_csv('a1_rgdpna_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('c2_laendercode_stage_v2.csv', header=0, encoding='utf-8')
df_4c = pd.read_csv('fragestellung_4_top4_laender.csv', header=0, encoding='utf-8')

#   verbindet beide datensets - über die iso-3 kennzeichnung wird das bip dem ganzen ländername zugewiesen
df_j = pd.merge(df_r, df_k, left_on='RegionCode', right_on='ISO-3', how='inner')
df_j.head()
df_4c.head()


#   beseitigt überflüssige spalten
df_j = df_j.drop(columns=["ISO-3", "RegionCode", "VariableCode"])
df_4c = df_4c.drop(columns="Anlass")

df_j.head()
df_4c.head()

#   auswahl der länder für die anaylse -> findings aus fragestellung_1:
#   1. usa 2. frankreich 3. italien 4. deutschland

df_usa = df_j[df_j['Land'] == 'USA']
df_date_usa = df_4c['Jahr'][(df_4c.Land_code == "USA") & ((df_4c.Jahr > 1949) & (df_4c.Jahr < 2020))]

df_fr = df_j[df_j['Land'] == 'Frankreich']
df_date_fr = df_4c['Jahr'][(df_4c.Land_code == "FRA") & ((df_4c.Jahr > 1949) & (df_4c.Jahr < 2020))]

df_it = df_j[df_j['Land'] == 'Italien']
df_date_it = df_4c['Jahr'][(df_4c.Land_code == "ITA") & ((df_4c.Jahr > 1949) & (df_4c.Jahr < 2020))]

df_de = df_j[df_j['Land'] == 'Deutschland']
df_date_de = df_4c['Jahr'][(df_4c.Land_code == "DEU") & ((df_4c.Jahr > 1949) & (df_4c.Jahr < 2020))]

df_usa.head()
df_fr.head()
df_it.head()
df_date_de.head()

#   erstellt ein plot von den bip über die zeit pro land
#   anschliessend wird der plot als png abgespeichert, für später zum excel file
#   usa
df_usa.plot(x='YearCode', y='AggValue', marker='', color='goldenrod', linewidth=1.0, figsize=(8,5))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of US GDP')
plt.savefig('fragestellung_4_usa_bip_time_series')
#   fr
df_fr.plot(x='YearCode', y='AggValue', marker='', color='steelblue', linewidth=1.0, figsize=(8,5))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of french GDP')
plt.savefig('fragestellung_4_frankreich_bip_time_series')
#   it
df_it.plot(x='YearCode', y='AggValue', marker='', color='yellowgreen', linewidth=1.0, figsize=(8,5))
plt.xlabel('year')
plt.ylabel('USD')
plt.title('Time Series of italian GDP')
plt.savefig('fragestellung_4_italien_bip_time_series')
#   de
df_de.plot(x='YearCode', y='AggValue', marker='', color='dimgray', linewidth=1.0, figsize=(8,5))
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

#   usa
plt.figure(1, figsize=(8, 5))
plt.plot(df_usa['YearCode'], usa_detrended, label="GDP_detrended", color='navajowhite', linewidth=0.5)
x = df_date_usa.tolist()
for a in x: plt.axvline(a, linewidth=0.5)
plt.title('Detrended Time Series of US GDP - with marked sports events')
plt.savefig('fragestellung_4_usa_time_series_analyse')
plt.show()

#   fr
plt.figure(2, figsize=(8, 5))
plt.plot(df_fr['YearCode'], fr_detrended, label="GDP_detrended", color='lightsteelblue', linewidth=0.5)
x = df_date_fr.tolist()
for a in x: plt.axvline(a, linewidth=0.5)
plt.title('Detrended Time Series of French GDP - with marked sports events')
plt.savefig('fragestellung_4_fr_time_series_analyse')
plt.show()

#   it
plt.figure(3, figsize=(8, 5))
plt.plot(df_it['YearCode'], it_detrended, label="GDP_detrended", color='darkseagreen', linewidth=0.5)
x = df_date_it.tolist()
for a in x: plt.axvline(a, linewidth=0.5)
plt.title('Detrended Time Series of Italian GDP - with marked sports events')
plt.savefig('fragestellung_4_it_time_series_analyse')

#   de
plt.figure(4, figsize=(8, 5))
plt.plot(df_de['YearCode'], de_detrended, label="GDP_detrended", color='slategray', linewidth=0.5)
x = df_date_de.tolist()
for a in x: plt.axvline(a, linewidth=0.5)
plt.title('Detrended Time Series of German GDP - with marked sports events')
plt.savefig('fragestellung_4_de_time_series_analyse')

#   fügt die plots png in ein excel sheet ein
workbook = xlsxwriter.Workbook('Result_Question_04.xlsx')

worksheet = workbook.add_worksheet("usa")
worksheet.insert_image('B2', 'fragestellung_4_usa_bip_time_series.png')
worksheet.insert_image('O2', 'fragestellung_4_usa_time_series_analyse.png')

worksheet = workbook.add_worksheet("fr")
worksheet.insert_image('B2', 'fragestellung_4_frankreich_bip_time_series.png')
worksheet.insert_image('O2', 'fragestellung_4_fr_time_series_analyse.png')

worksheet = workbook.add_worksheet("it")
worksheet.insert_image('B2', 'fragestellung_4_italien_bip_time_series.png')
worksheet.insert_image('O2', 'fragestellung_4_it_time_series_analyse.png')

worksheet = workbook.add_worksheet("de")
worksheet.insert_image('B2', 'fragestellung_4_deutschland_bip_time_series.png')
worksheet.insert_image('O2', 'fragestellung_4_de_time_series_analyse.png')

workbook.close()


#### lessons learned
# -
