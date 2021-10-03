"""
Get history weather data from openweathermap for the specific cities and chosen weather variables and save the resulting
dataframes as pickles.
"""

from ML_Model_Data.A_Weather_Data_Call import get_history
from ML_Model_Data.constants import (
    API_KEY,
    COL_LIST,
    START_DATE_WEATHER_HISTORY,
    STUTTGART,
    FREIBURG,
    MANNHEIM,
    RAVENSBURG
)
import pandas as pd

#%%
def make_history_weather_df():
    # Erstellen eines gesamthaften Dateframes mit den historischen Wetterdaten am jeweiligen Standort
    history_wetterdaten_Stuttgart = pd.DataFrame()
    history_wetterdaten_Freiburg = pd.DataFrame()
    history_wetterdaten_Mannheim = pd.DataFrame()
    history_wetterdaten_Ravensburg = pd.DataFrame()

    # Schleife bezieht die historischen Wettervorhersagen in Wochenabschnitten für die jeweiligen Städte und erstellt ein gesamthaftes DF
    for x in range(0, 51):
        # Stuttgart Wetter
        history_wetterdaten_week_Stuttgart = get_history(API_KEY, STUTTGART, (START_DATE_WEATHER_HISTORY + x * 604800), 168, COL_LIST)
        history_wetterdaten_Stuttgart = pd.concat([history_wetterdaten_Stuttgart, history_wetterdaten_week_Stuttgart], axis=0, ignore_index=True)

        # Freiburg Wetter
        history_wetterdaten_week_Freiburg = get_history(API_KEY, FREIBURG, (START_DATE_WEATHER_HISTORY + x * 604800), 168, COL_LIST)
        history_wetterdaten_Freiburg = pd.concat([history_wetterdaten_Freiburg, history_wetterdaten_week_Freiburg], axis=0, ignore_index=True)

        # Mannheim Wetter
        history_wetterdaten_week_Mannheim = get_history(API_KEY, MANNHEIM, (START_DATE_WEATHER_HISTORY + x * 604800), 168, COL_LIST)
        history_wetterdaten_Mannheim = pd.concat([history_wetterdaten_Mannheim, history_wetterdaten_week_Mannheim], axis=0, ignore_index=True)

        # Ravensburg Wetter
        history_wetterdaten_week_Ravensburg = get_history(API_KEY, RAVENSBURG, (START_DATE_WEATHER_HISTORY + x * 604800), 168, COL_LIST)
        history_wetterdaten_Ravensburg = pd.concat([history_wetterdaten_Ravensburg, history_wetterdaten_week_Ravensburg], axis=0, ignore_index=True)

    # Dataframes als Pickle abspeichern
    pd.to_pickle(history_wetterdaten_Stuttgart, "../data/history_weather_stuttgart_28Sep2020_19Sep_2020_test.pkl")
    pd.to_pickle(history_wetterdaten_Freiburg, "../data/history_weather_freiburg_28Sep2020_19Sep_2020_test.pkl")
    pd.to_pickle(history_wetterdaten_Mannheim, "../data/history_weather_mannheim_28Sep2020_19Sep_2020_test.pkl")
    pd.to_pickle(history_wetterdaten_Ravensburg, "../data/history_weather_ravensburg_28Sep2020_19Sep_2020_test.pkl")

if __name__ == "__main__":
    make_history_weather_df()
