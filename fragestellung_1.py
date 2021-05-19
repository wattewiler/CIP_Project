################################# FRAGESTELLUNG 1 #################################
# Welches Land war zwischen 1950-2019 am häufigsten Gastgeber eines
# Sportgrossanlasses (Sommer- und Winterolympiade, Fussballweltmeisterschaft)?


# Benötigte Libraries laden
import pandas as pd

# Datenquellen werden eingelesen
df_wm = pd.read_csv('b1_wm_stage.csv', header=0, encoding='utf-8')
df_wo = pd.read_csv('b2_wolympics_stage.csv', header=0, encoding='utf-8')
df_so = pd.read_csv('b3_solympics_stage.csv', header=0, encoding='utf-8')
df_lc = pd.read_csv('c2_laendercode_stage.csv', header=0, encoding='utf-8')

# Der Outputname des Excels definiert
xlsx_output_name = 'Result_Question_01.xlsx'

# Erste Inspektion der Daten
df_wm.info()
df_wo.info()
df_so.info()
df_lc.info()

# Aufbereitung Laenderkürzel-Dataset, um den anderen Datasets zu entsprechen
df_lc_new = df_lc.rename(columns={'ISO-3' : 'Land_code'})

# Aufbereitung des Datasets Fussballweltmeisterschaften (Neuanordnung Spalten, neue Spalte für Art des Anlasses)
df_wm_new = df_wm[['Jahr', 'Land']]
df_wm_new['Anlass'] = 'Fussballweltmeisterschaft'

# Aufbereitung des Datasets Olympische Sommerspiele (Join mit CSV der Ländercodes, danach neu anordnen der Spalten)
df_so_new = pd.merge(df_so, df_lc_new, on='Land_code', how='inner')
df_so_new.pop('Land_code')
df_so_new = df_so_new[['Jahr', 'Land', 'Anlass']]

# Aufbereitung des Datasets Olympische Winterspiele (Join mit CSV der Ländercodes, danach neu anordnen der Spalten)
df_wo_new = pd.merge(df_wo, df_lc_new, on='Land_code', how='inner')
df_wo_new.pop('Land_code')
df_wo_new = df_wo_new[['Jahr', 'Land', 'Anlass']]

# Zusammenführen der drei Datasets Sportanlässe und sortieren nach Jahr
df_concatenated = pd.concat([df_wo_new, df_so_new, df_wm_new])
df_concatenated = df_concatenated.sort_values(by=['Jahr'],ignore_index=True)

# Bevor das XSLX generiert wird, werden Filter angewendet und die Werte gezählt & nach der Anzahl sortiert
df_final = df_concatenated.loc[(df_concatenated['Jahr'] > 1950) & (df_concatenated['Jahr'] < 2019)]
df_final = df_concatenated['Land'].value_counts(sort=True)

# Schlussendlich wird die Auswertung in ein Excelfile geschrieben
df_final.to_excel(xlsx_output_name)

#### LESSONS LEARNED ####
# Es ist sehr wichtig, dass gleich zu Beginn des Scraping definiert ist, wie die exportierten und aufbereiteten Daten
# aussehen sollen. So hätte ich mir einige Arbeitsschritte ersparen können, wenn der Teamkollege und ich bereits
# von Anfang an das gleiche Schema verfolgt hätten. So benötigte es meinerseits einige Aufbereitungsschritte mehr,
# die eigentlich bereits im Cleaning-Step erfolgt hätte können.
# GitHub mit der zentralisierten Repository und der Version Control hat uns sehr geholfen, jederzeit "Herr" unserer
# Daten und des Codes zu sein.