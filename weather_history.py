from weather_to_pandas import get_history
import pandas as pd

#%% Allegemeine Parameter
city_name = "Stuttgart,DE"
api_key = "7660e06da8e929a654c00a31197de127"
start_date_history = 1601510400  # Friday, 1. October 2020 00:00:00 UTC

# Spaltenliste welche die jeweiligen Spalten in den History und Forecast Dataframes letztendlich darstellt
col_list = ["date_utc",
            "city.id",
            'main.temp', 'main.feels_like', 'main.pressure', 'main.humidity',
            'wind.speed', 'wind.deg',
            'clouds.all',
            'weather.main',
            'weather.description']

#%% Erstellen eines gesamthaften Dateframes mit den historischen Wetterdaten am jeweiligen Standort
history_wetterdaten = pd.DataFrame()
for x in range(0, 5):
    history_wetterdaten_week = get_history(api_key, city_name, (start_date_history + x * 604800), 168, col_list)
    history_wetterdaten = pd.concat([history_wetterdaten, history_wetterdaten_week], axis=0, ignore_index=True)
