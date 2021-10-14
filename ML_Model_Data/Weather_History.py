"""
Get history weather data from openweathermap for the specific cities and chosen weather variables and save the resulting
dataframes as pickles.
"""

from ML_Model_Data.Weather_Data_Call import HistoryWeather
from ML_Model_Data.constants import (
    COL_LIST,
    START_DATE_WEATHER_HISTORY,
    START_DATE_WEATHER_HISTORY_TEST,
    STUTTGART,
    FREIBURG,
    MANNHEIM,
    RAVENSBURG
)
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
        history_wetterdaten_week_Stuttgart = HistoryWeather(STUTTGART, COL_LIST, (start_date + x * 604800), 168).get_weather_history()
        history_wetterdaten_Stuttgart = pd.concat([history_wetterdaten_Stuttgart, history_wetterdaten_week_Stuttgart], axis=0, ignore_index=True)

        # Freiburg Wetter
        history_wetterdaten_week_Freiburg = HistoryWeather(FREIBURG, COL_LIST, (start_date + x * 604800), 168).get_weather_history()
        history_wetterdaten_Freiburg = pd.concat([history_wetterdaten_Freiburg, history_wetterdaten_week_Freiburg], axis=0, ignore_index=True)

        # Mannheim Wetter
        history_wetterdaten_week_Mannheim = HistoryWeather(MANNHEIM, COL_LIST, (start_date + x * 604800), 168).get_weather_history()
        history_wetterdaten_Mannheim = pd.concat([history_wetterdaten_Mannheim, history_wetterdaten_week_Mannheim], axis=0, ignore_index=True)

        # Ravensburg Wetter
        history_wetterdaten_week_Ravensburg = HistoryWeather(RAVENSBURG, COL_LIST, (start_date + x * 604800), 168).get_weather_history()
        history_wetterdaten_Ravensburg = pd.concat([history_wetterdaten_Ravensburg, history_wetterdaten_week_Ravensburg], axis=0, ignore_index=True)

    # Dataframes als Pickle abspeichern
    base_path = Path(__file__).parent
    test = "_test"
    pd.to_pickle(history_wetterdaten_Stuttgart, (base_path / f"../data/01_Base_Data/history_weather_stuttgart_28Sep2020_19Sep_2020{test}.pkl").resolve())
    # pd.to_pickle(history_wetterdaten_Stuttgart, f"../data/01_Base_Data/history_weather_stuttgart_28Sep2020_19Sep_2020{test}.pkl")
    pd.to_pickle(history_wetterdaten_Freiburg, f"../data/01_Base_Data/history_weather_freiburg_28Sep2020_19Sep_2020{test}.pkl")
    pd.to_pickle(history_wetterdaten_Mannheim, f"../data/01_Base_Data/history_weather_mannheim_28Sep2020_19Sep_2020{test}.pkl")
    pd.to_pickle(history_wetterdaten_Ravensburg, f"../data/01_Base_Data/history_weather_ravensburg_28Sep2020_19Sep_2020{test}.pkl")

if __name__ == "__main__":
    make_history_weather_df(weeks=2, start_date=START_DATE_WEATHER_HISTORY_TEST)

    # df1 = pd.read_pickle("../data/01_Base_Data/history_weather_stuttgart_28Sep2020_19Sep_2020_test.pkl")
    # df2 = pd.read_pickle("../data/01_Base_Data/history_weather_freiburg_28Sep2020_19Sep_2020_test.pkl")
    # df3 = pd.read_pickle("../data/01_Base_Data/history_weather_mannheim_28Sep2020_19Sep_2020_test.pkl")
    # df4 = pd.read_pickle("../data/01_Base_Data/history_weather_ravensburg_28Sep2020_19Sep_2020_test.pkl")
