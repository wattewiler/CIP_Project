#### frage 4: Gibt es eine statistisch feststellbare, signifikante Korrelation zwischen der Durchführung von...
####            Sportgrossanlässen und der Veränderung des BIPs der Gastgebernation?
####
#### input: 'länderkode_stage.csv', 'rgdpna.csv'
#### output:
#### method: step 1: verbinden von 'rgdpna.csv' via länderkürzel-ländername von 'länderkode_stage.csv'
####         step 2: auswahl von 4 ländern; 2 mit vielen sportgrossanlasereignissen, 2 mit niedrigem BIP
####         Step 3: time series analysis, detrending, ermittlung von outlier und abgleich mit sportevents
#### laypout df: ländername, jahr, bip

#load libraries and set genreals
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

#for ml, not working yet
from sklearn.preprocessing import StandardScaler
from sklearn import svm
#


#load data
df_r = pd.read_csv('rgdpna.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('länderkode_stage.csv', header=0, encoding='utf-8')

#merge both data frames
df_j = pd.merge(df_r, df_k, left_on='RegionCode', right_on='ISO-3', how='inner')
df_j = df_j.drop(columns="ISO-3")
df_j = df_j.drop(columns="RegionCode")
df_j = df_j.drop(columns="VariableCode")

df_j.head()

#select country, from question 1: find top two countries:
df_c1 = df_j[df_j['Land'] == 'Frankreich']
df_c1.head()

#plot time series
df_c1.plot(x='YearCode', y='AggValue', marker='o', color='goldenrod', linewidth=5.0, figsize=(30,15))
plt.xlabel('Date time')
plt.ylabel('Price in USD')
plt.title('Time Series of French GDP')

#detrending of time series
x_detrended = signal.detrend(df_c1['AggValue'])
x_detrended = signal.detrend(x_detrended)

plt.figure(figsize=(30 , 15))
#plt.plot(df_c1['YearCode'], df_c1['AggValue'], label="GDP") #left out in order to better plot detrended TS
plt.plot(df_c1['YearCode'], x_detrended, label="GDP_detrended", color='lightsteelblue', linewidth=5.0, linestyle='dotted')
plt.legend(loc='best')
plt.show()


##############################################################ml_tries
df = df_c1.sort_values('YearCode')
df['date_time_int'] = df.YearCode.astype(np.int64)
fig, ax = plt.subplots(figsize=(30,15))
a = df.loc[df['anomaly1'] == 1, ['date_time_int', 'price_usd']] #anomaly

ax.plot(df['date_time_int'], df['price_usd'], color='blue', label='Normal')
ax.scatter(a['date_time_int'],a['price_usd'], color='red', label='Anomaly')
plt.xlabel('Date Time Integer')
plt.ylabel('price in USD')
plt.legend()
plt.show()

#Support Vector Machine-Based Anomaly Detection - OneClassSVM
data = df_c1[['AggValue']]
scaler = StandardScaler()
np_scaled = scaler.fit_transform(data)
data = pd.DataFrame(np_scaled)
# train oneclassSVM
model = svm.OneClassSVM(nu=0.2, kernel="rbf", gamma=0.1)
model.fit(data)
df = pd.DataFrame()
df['anomaly3'] = pd.Series(model.predict(data))

fig, ax = plt.subplots(figsize=(30,15))
a = df.loc[df['anomaly3'] == -1, ['YearCode', 'AggValue']] #anomaly

ax.plot(df['YearCode'], df['AggValue'], color='blue')
ax.scatter(a['YearCode'],a['AggValue'], color='red')
plt.show()

#Anomaly Detection Toolkit (ADTK)
