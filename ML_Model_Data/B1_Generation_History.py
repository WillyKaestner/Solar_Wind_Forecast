"""
Transform the history energy generation data from Transnet BW Regelzone to hourly data and save as pandas pickle.
"""

import pandas as pd

#%%
def generate_history_energy_df():
    erzeugung_bw = pd.read_csv("../data/Realisierte_Erzeugung_202009270000_202109202359.csv", sep=";")

    # Aus den Datum und Uhrzeit Spalten die Strings nehmen und Datetime Index erstellen
    erzeugung_bw["Datum_UTC+1"] = erzeugung_bw[["Datum", "Uhrzeit"]].agg(" ".join, axis=1)
    erzeugung_bw["Datum_UTC+1"] = pd.to_datetime(erzeugung_bw["Datum_UTC+1"], format='%d.%m.%Y %H:%M')
    erzeugung_bw.drop(columns=["Datum", "Uhrzeit"], inplace=True)

    # Datum als Index setzen und mittels resample von 0,25h auf 1h Auflösung aggregieren
    erzeugung_bw.set_index("Datum_UTC+1", inplace=True)
    erzeugung_bw_hourly = erzeugung_bw.resample('H').sum()

    # Zeit um eine Stunde nach hinten verschieben aufgrund der UTC+1 Zeitzone
    # -> https://towardsdatascience.com/all-the-pandas-shift-you-should-know-for-data-analysis-791c1692b5e
    # Auswahl der Erzeugungsdaten für den Zeitraum in dem wir auch historische Wetterdaten zur Verfügung haben
    erzeugung_bw_hourly_UTC = erzeugung_bw_hourly.shift(periods=-1, freq='H')
    erzeugung_bw_hourly_UTC_Datumauswahl = erzeugung_bw_hourly_UTC.loc["2020-09-28":"2021-09-19"]

    # Export des Dataframes als Pickle
    pd.to_pickle(erzeugung_bw_hourly_UTC_Datumauswahl, "../data/history_erzeugung_bw_28Sep2020_19Sep_2020.pkl")

if __name__ == "__main__":
    generate_history_energy_df()
