"""
Get the weather and generation data for the specific cities in Baden-Württemberg which is needed for the ML Model implementation save the resulting
dataframes as pickles.
"""

from Weather_And_Generation.Weather_Data_Call import HistoryWeather
from Weather_And_Generation.constants import (
    COL_LIST,
    START_DATE_WEATHER_HISTORY,
    START_DATE_WEATHER_HISTORY_TEST,
    STUTTGART,
    FREIBURG,
    MANNHEIM,
    RAVENSBURG
)
from Weather_And_Generation.Generation_Data_Call import SmardGenerationData

import pandas as pd
from pathlib import Path

#%%
def make_history_weather_df(weeks: int, start_date: int):
    # Erstellen eines gesamthaften Dateframes mit den historischen Wetterdaten am jeweiligen Standort
    history_wetterdaten_Stuttgart = pd.DataFrame()
    history_wetterdaten_Freiburg = pd.DataFrame()
    history_wetterdaten_Mannheim = pd.DataFrame()
    history_wetterdaten_Ravensburg = pd.DataFrame()

    # Schleife bezieht die historischen Wettervorhersagen in Wochenabschnitten für die jeweiligen Städte und erstellt ein gesamthaftes DF
    for x in range(0, weeks):
        # Stuttgart Wetter
        history_wetterdaten_week_Stuttgart = HistoryWeather(STUTTGART, COL_LIST, (start_date + x * 604800), 168).get_weather_data_for_ML_model()
        history_wetterdaten_Stuttgart = pd.concat([history_wetterdaten_Stuttgart, history_wetterdaten_week_Stuttgart], axis=0, ignore_index=True)

        # Freiburg Wetter
        history_wetterdaten_week_Freiburg = HistoryWeather(FREIBURG, COL_LIST, (start_date + x * 604800), 168).get_weather_data_for_ML_model()
        history_wetterdaten_Freiburg = pd.concat([history_wetterdaten_Freiburg, history_wetterdaten_week_Freiburg], axis=0, ignore_index=True)

        # Mannheim Wetter
        history_wetterdaten_week_Mannheim = HistoryWeather(MANNHEIM, COL_LIST, (start_date + x * 604800), 168).get_weather_data_for_ML_model()
        history_wetterdaten_Mannheim = pd.concat([history_wetterdaten_Mannheim, history_wetterdaten_week_Mannheim], axis=0, ignore_index=True)

        # Ravensburg Wetter
        history_wetterdaten_week_Ravensburg = HistoryWeather(RAVENSBURG, COL_LIST, (start_date + x * 604800), 168).get_weather_data_for_ML_model()
        history_wetterdaten_Ravensburg = pd.concat([history_wetterdaten_Ravensburg, history_wetterdaten_week_Ravensburg], axis=0, ignore_index=True)

    # Dataframes als Pickle abspeichern
    base_path = Path(__file__).parent
    test = "_test"
    pd.to_pickle(history_wetterdaten_Stuttgart, (base_path / f"../data/01_Base_Data/history_weather_stuttgart_28Sep2020_19Sep_2020{test}.pkl").resolve())
    pd.to_pickle(history_wetterdaten_Freiburg, (base_path / f"../data/01_Base_Data/history_weather_freiburg_28Sep2020_19Sep_2020{test}.pkl").resolve())
    pd.to_pickle(history_wetterdaten_Mannheim, (base_path / f"../data/01_Base_Data/history_weather_mannheim_28Sep2020_19Sep_2020{test}.pkl").resolve())
    pd.to_pickle(history_wetterdaten_Ravensburg, (base_path / f"../data/01_Base_Data/history_weather_ravensburg_28Sep2020_19Sep_2020{test}.pkl").resolve())

if __name__ == "__main__":
    # Wetterdaten über 50 Wochen für die jeweiligen Städte in BW abrufen und abspeichern
    make_history_weather_df(weeks=2, start_date=START_DATE_WEATHER_HISTORY_TEST)

    # Erzeugungsdaten aus Baden-Württemberg einlesen und abspeichern
    BW_28Sep2020_19Sep2021 = SmardGenerationData(start_date="28Sep2020",
                                                 end_date="19Sep2021",
                                                 regelzone="bw")
    Generation_BW = BW_28Sep2020_19Sep2021.read_generation_data_from_file("01_Base_Data/Realisierte_Erzeugung_202009270000_202109202359.csv")
    BW_28Sep2020_19Sep2021.save_generation_data_as_pickle(Generation_BW)
