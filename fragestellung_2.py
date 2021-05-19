#### frage 2: Welcher Kontinent verzeichnet den grössten BIP-Zuwachs in der Periode von 2000-2019?
####
#### input: c1_country_stage.csv, c2_laendercode_stage.csv, a1_rgdpna_stage.csv
#### output: Result_Question_02.xlsx
#### process: verbinden von c1_country_stage.csv mit a1_rgdpna_stage.csv via länderkürzel-ländername von c2_laendercode_stage.csv

#   ladet die Libraries
import pandas as pd
from matplotlib import pyplot as plt
import xlsxwriter


#   ladet die csv's
df_c = pd.read_csv('c1_country_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('c2_laendercode_stage.csv', header=0, encoding='utf-8')
df_r = pd.read_csv('a1_rgdpna_stage.csv', header=0, encoding='utf-8')

#   erste daten-inspektion
df_c.head()
df_c.info()
df_k.head()
df_k.info()
df_r.head()
df_r.info()

#   untfernt unnötige spalte
df_r = df_r.drop(columns="VariableCode")

#   verbindet die dataframes zusammen
df_joined_1 = pd.merge(df_c, df_k, on='Land', how='inner')
df_joined_1.head()
df_joined_1.info()

# -> mergen führt zu datenverlust, ~ 60 einträge. es hat sich gezeigt, dass die länderbennen in den...
#    daten nicht konsistent ist. deswegen ist ein manuelles cleaning nötig
################################################################################################
#### input: c2_laendercode_stage.csv
#### process: manuelle verarbeitung
#### output: c2_laendercode_stage_v2.csv

#   findet die unterschiedlichen Ländernamen - vergleich "country_stage" mit "länderkode_stage"
for l in df_k['Land']:
    if not df_c['Land'].str.contains(l).any():
        print(l)

df_k = pd.read_csv('c2_laendercode_stage_v2.csv', header=0, encoding='utf-8')
df_k.info()
#   -> mergen führt jetzt nur noch zu einem verlust von ~ 20 einträge. diese einträge sind z.b. kleine
#       inselgruppen etc., die nicht klar zuzuweisen sind

df_joined_1 = pd.merge(df_c, df_k, on='Land', how='inner')
df_joined_1.head()
df_joined_1.info()
################################################################################################
#   zusammenführen der daten, diesmal mit dem manuell korrigiertem file
df_joined_2 = pd.merge(df_joined_1, df_r, left_on='ISO-3', right_on='RegionCode', how='inner')
df_joined_2.head()
df_joined_2.info()

#   reindexierung des dataframe, dann ein groupby() mit sum()
#       spalten ohne numerischen wert gehen durch den sum() prozess verloren, was aber gerade gewollt ist
df_i2 = df_joined_2.set_index(['Kontinent', 'YearCode'])
new_df2 = df_i2.groupby(level= ['Kontinent', 'YearCode']).sum()

#   reset des index -> indexen werden wieder zu spalten
df_res2 = new_df2.reset_index()
df_res2.info()

#   erste datenanalyse - gdp-time by continent
df_piv = df_res2.pivot(index='YearCode', columns='Kontinent', values='AggValue')
df_piv.plot()
plt.title("gdp_over_time_by_continent")
#safe plot as png
plt.savefig('fragestellung_2_gdp_time_by_continent')

#######################
#   behaltet nur die zeilen mit dem jahr 2000 oder 2019
df_j = df_joined_2.drop(df_joined_2[(df_joined_2.YearCode != 2000) & (df_joined_2.YearCode != 2019)].index)
df_j.head()
df_j.info()

#   reindexierung des dataframe, dann ein groupby() mit sum()
df_i = df_j.set_index(['Kontinent', 'YearCode'])
new_df = df_i.groupby(level= ['Kontinent', 'YearCode']).sum()
#   reset des index -> indexen werden wieder zu spalten
df_res = new_df.reset_index()

#   erstelllt eine funktion das den absoluten unterschied des bip rechnet
def delta_gdp(name):
    d = float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2019)]) - \
        float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2000)])
    return d

#   erstelllt eine funktion das den relativen unterschied des bip rechnet
def delta_gdp_r(name):
    d = float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2019)]) / \
        float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2000)])
    return d

#   erstellt neuen datenset, mit werten aus der funktion
a = {"Afrika": [delta_gdp("Afrika")],
    "Asien": [delta_gdp("Asien")],
    "Australien": [delta_gdp("Australien")],
    "Europa": [delta_gdp("Europa")],
    "Europa/Asien": [delta_gdp("Europa/Asien")],
    "Nordamerika": [delta_gdp("Nordamerika")],
    "Suedamerika": [delta_gdp("Suedamerika")]
     }
a_df = pd.DataFrame(a)

b = {"Afrika": [delta_gdp_r("Afrika")],
    "Asien": [delta_gdp_r("Asien")],
    "Australien": [delta_gdp_r("Australien")],
    "Europa": [delta_gdp_r("Europa")],
    "Europa/Asien": [delta_gdp_r("Europa/Asien")],
    "Nordamerika": [delta_gdp_r("Nordamerika")],
    "Suedamerika": [delta_gdp_r("Suedamerika")]
     }
b_df = pd.DataFrame(b)

#   tauscht index mit spalten und stellt das bip absteigend
xx = b_df.T
x1 = xx.sort_values(by=0)
x2 = x1.reset_index()
#   ersellt einen boxplot und speichert dieser als png file
x2.columns = ["Kontinent", "GDP"]
x2.plot.bar(x='Kontinent', y='GDP', color = "green")
plt.xticks(rotation=20, horizontalalignment="center")
plt.title('relative change of GDP (2000-2019)')

#safe plot as png
plt.savefig('fragestellung_2_relative_change_of_gdp (2000-2019)')

#   tauscht index mit spalten und stellt das bip absteigend
yy = a_df.T
y1 = yy.sort_values(by=0)
y2 = y1.reset_index()
#   ersellt einen boxplot und speichert dieser als png file
y2.columns = ["Kontinent", "GDP"]
y2.plot.bar(x='Kontinent', y='GDP', color = "gold")
plt.xticks(rotation=20, horizontalalignment="center")
plt.title('fragestellung_2_absolute_change_of_gdp (2000-2019)')

#safe plot as png
plt.savefig('fragestellung_2_absolute_change_of_gdp (2000-2019)')

#   fügt die boxplot png in ein excel sheet ein
workbook = xlsxwriter.Workbook('Result_Question_02.xlsx')
worksheet = workbook.add_worksheet()
worksheet.insert_image('B2', 'fragestellung_2_gdp_time_by_continent.png')
worksheet.insert_image('L2', 'fragestellung_2_absolute_change_of_gdp.png')
worksheet.insert_image('V2', 'fragestellung_2_relative_change_of_gdp.png')

workbook.close()

#### lessons learned
# - daten mit wissenschaftlicher notation (3.45e+08) kann durch ein float type richtig interpretiert werden
# - gruppieren mit sum() kann zu spaltenverluste führen (nichtnumerischen werte)