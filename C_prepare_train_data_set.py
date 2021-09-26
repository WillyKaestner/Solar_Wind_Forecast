import pandas as pd

#%% Ausgangsdaten einlesen. Wetterdaten und Erzeugungsdaten
history_wetterdaten_Stuttgart = pd.read_pickle("data/history_weather_stuttgart_28Sep2020_19Sep_2020.pkl")
history_wetterdaten_Freiburg = pd.read_pickle("data/history_weather_freiburg_28Sep2020_19Sep_2020.pkl")
history_wetterdaten_Mannheim = pd.read_pickle("data/history_weather_mannheim_28Sep2020_19Sep_2020.pkl")
history_wetterdaten_Ravensburg = pd.read_pickle("data/history_weather_ravensburg_28Sep2020_19Sep_2020.pkl")

history_erzeugung_bw = pd.read_pickle("data/history_erzeugung_bw_28Sep2020_19Sep_2020.pkl")

# Datetime Index der Erzeugungsdaten in Spalte verschieben
history_erzeugung_bw.reset_index(inplace=True)

# Solar und Wind Train Dataframe initiieren
train_solar = pd.DataFrame(history_wetterdaten_Stuttgart["date_utc"])
train_wind = pd.DataFrame(history_wetterdaten_Stuttgart["date_utc"])

# Erzeugungsdaten hinzufügen
train_solar["PV[MWh]"] = history_erzeugung_bw["Photovoltaik[MWh]"]
train_wind["Wind_Onshore[MWh]"] = history_erzeugung_bw["Wind Onshore[MWh]"]

# Monats und Stunden Spalte hinzufügen
train_solar["month"] = train_solar["date_utc"].map(lambda x: x.month)
train_solar["hour"] = train_solar["date_utc"].map(lambda x: x.hour)

train_wind["month"] = train_wind["date_utc"].map(lambda x: x.month)
train_wind["hour"] = train_wind["date_utc"].map(lambda x: x.hour)

# Stadtnamen als Prefix in jeder Spalte
history_wetterdaten_Stuttgart.columns = ['STG_' + str(col) for col in history_wetterdaten_Stuttgart.columns]
history_wetterdaten_Freiburg.columns = ['FRB_' + str(col) for col in history_wetterdaten_Freiburg.columns]
history_wetterdaten_Mannheim.columns = ['MAN_' + str(col) for col in history_wetterdaten_Mannheim.columns]
history_wetterdaten_Ravensburg.columns = ['RAV_' + str(col) for col in history_wetterdaten_Ravensburg.columns]

# Wetterdaten gesamthaft den bein train Datensätzen hinzufügen
train_solar = pd.concat([train_solar,
                         history_wetterdaten_Stuttgart.iloc[:, 2:],
                         history_wetterdaten_Freiburg.iloc[:, 2:],
                         history_wetterdaten_Mannheim.iloc[:, 2:],
                         history_wetterdaten_Ravensburg.iloc[:, 2:]],
                        axis=1)

train_wind = pd.concat([train_wind,
                        history_wetterdaten_Stuttgart.iloc[:, 2:],
                        history_wetterdaten_Freiburg.iloc[:, 2:],
                        history_wetterdaten_Mannheim.iloc[:, 2:],
                        history_wetterdaten_Ravensburg.iloc[:, 2:]],
                       axis=1)

# Date_utc Spalte in den beiden train Datensätzen löschen
train_solar.drop(columns=["date_utc"], inplace=True)
train_wind.drop(columns=["date_utc"], inplace=True)

# Exportieren der train Dataframes
train_solar.to_pickle("data/train_solar.pkl")
train_wind.to_pickle("data/train_wind.pkl")
