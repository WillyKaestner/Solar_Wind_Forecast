from A_weather_to_pandas import get_history
import pandas as pd

#%% Allgemeine Parameter
Stuttgart = "Stuttgart,DE"
Freiburg = "Freiburg,DE"
Mannheim = "Mannheim,DE"
Ravensburg = "Ravensburg,DE"

api_key = "7660e06da8e929a654c00a31197de127"
# start_date_history = 1601510400  # Friday, 1. October 2020 00:00:00 UTC
start_date_history = 1601251200  # Monday, 28. September 2020 00:00:00

# Spaltenliste welche die jeweiligen Spalten in den History und Forecast Dataframes letztendlich darstellt
col_list = ["date_utc",
            "city.id",
            'main.temp', 'main.feels_like', 'main.pressure', 'main.humidity',
            'wind.speed', 'wind.deg',
            'clouds.all',
            'weather.main',
            'weather.description']

#%% Erstellen eines gesamthaften Dateframes mit den historischen Wetterdaten am jeweiligen Standort
history_wetterdaten_Stuttgart = pd.DataFrame()
history_wetterdaten_Freiburg = pd.DataFrame()
history_wetterdaten_Mannheim = pd.DataFrame()
history_wetterdaten_Ravensburg = pd.DataFrame()

# Schleife bezieht die historischen Wettervorhersagen in Wochenabschnitten für die jeweiligen Städte und erstellt ein gesamthaftes DF
for x in range(0, 51):
    # Stuttgart Wetter
    history_wetterdaten_week_Stuttgart = get_history(api_key, Stuttgart, (start_date_history + x * 604800), 168, col_list)
    history_wetterdaten_Stuttgart = pd.concat([history_wetterdaten_Stuttgart, history_wetterdaten_week_Stuttgart], axis=0, ignore_index=True)

    # Freiburg Wetter
    history_wetterdaten_week_Freiburg = get_history(api_key, Freiburg, (start_date_history + x * 604800), 168, col_list)
    history_wetterdaten_Freiburg = pd.concat([history_wetterdaten_Freiburg, history_wetterdaten_week_Freiburg], axis=0, ignore_index=True)

    # Mannheim Wetter
    history_wetterdaten_week_Mannheim = get_history(api_key, Mannheim, (start_date_history + x * 604800), 168, col_list)
    history_wetterdaten_Mannheim = pd.concat([history_wetterdaten_Mannheim, history_wetterdaten_week_Mannheim], axis=0, ignore_index=True)

    # Ravensburg Wetter
    history_wetterdaten_week_Ravensburg = get_history(api_key, Ravensburg, (start_date_history + x * 604800), 168, col_list)
    history_wetterdaten_Ravensburg = pd.concat([history_wetterdaten_Ravensburg, history_wetterdaten_week_Ravensburg], axis=0, ignore_index=True)

# Dataframes als Pickle abspeichern
pd.to_pickle(history_wetterdaten_Stuttgart, "data/history_weather_stuttgart_28Sep2020_19Sep_2020.pkl")
pd.to_pickle(history_wetterdaten_Freiburg, "data/history_weather_freiburg_28Sep2020_19Sep_2020.pkl")
pd.to_pickle(history_wetterdaten_Mannheim, "data/history_weather_mannheim_28Sep2020_19Sep_2020.pkl")
pd.to_pickle(history_wetterdaten_Ravensburg, "data/history_weather_ravensburg_28Sep2020_19Sep_2020.pkl")
