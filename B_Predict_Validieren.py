import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%% Prognose Daten von Smard einlesen aus CSV Datei
erzeugung_bw = pd.read_csv("data/01_Forecast_Validation_Data/Realisierte_Erzeugung_202110050000_202110052359.csv", sep=";")

# Aus den Datum und Uhrzeit Spalten die Strings nehmen und Datetime Index erstellen
erzeugung_bw["Datum_UTC+1"] = erzeugung_bw[["Datum", "Uhrzeit"]].agg(" ".join, axis=1)
erzeugung_bw["Datum_UTC+1"] = pd.to_datetime(erzeugung_bw["Datum_UTC+1"], format='%d.%m.%Y %H:%M')
erzeugung_bw.drop(columns=["Datum", "Uhrzeit"], inplace=True)

# Datum als Index setzen und mittels resample von 0,25h auf 1h Auflösung aggregieren
erzeugung_bw.set_index("Datum_UTC+1", inplace=True)
#%%
# Die letzten 8 Zeilen löschen da sie leer sind
erzeugung_bw.drop(erzeugung_bw.tail(8).index, inplace=True)
# Daten in Float Werte ändern
cols = erzeugung_bw.columns
for col in cols:
    erzeugung_bw[col] = erzeugung_bw[col].astype(float)
erzeugung_bw_hourly = erzeugung_bw.resample('H').sum()

# Time Spalte hinzufügen
erzeugung_bw_hourly.reset_index(inplace=True)
erzeugung_bw_hourly["time (h)"] = erzeugung_bw_hourly["Datum_UTC+1"].dt.strftime('%m-%d %H:%M')

#%% Grafik
sns.set_theme()
fig, ax = plt.subplots(figsize=(12, 4))
sns.barplot(data=erzeugung_bw_hourly, x="time (h)", y="Photovoltaik[MWh]")
plt.setp(ax.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.show()
