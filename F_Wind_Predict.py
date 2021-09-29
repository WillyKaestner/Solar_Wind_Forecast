#%%
import pandas as pd
from joblib import load
from A_weather_to_pandas import get_forecast
import matplotlib.pyplot as plt
import seaborn as sns
#%%
#  Allgemeine Daten
api_key = "7660e06da8e929a654c00a31197de127"
time_steps = 48

# Wind ML Model einlesen
clf_wind = load("data/wind_model.joblib")

# Spaltenliste welche die jeweiligen Spalten in den History und Forecast Dataframes letztendlich darstellt
col_list = ['main.temp', 'main.feels_like', 'main.pressure', 'main.humidity',
            'wind.speed', 'wind.deg',
            'clouds.all',
            'weather.main']

# Städeliste
cities = ["Stuttgart,DE", "Freiburg,DE", "Mannheim,DE", "Ravensburg,DE"]
cities_prefix = {"Stuttgart,DE": "STG_", "Freiburg,DE": "FRB_", "Mannheim,DE": "MAN_", "Ravensburg,DE": "RAV_"}

# Weather Dataframe initialisieren
weather_forecast = pd.DataFrame()

# Datumsbereich bekommen, in Monat und Stunde aufteilen und als erste beiden Spalten definieren
date_range_df = get_forecast(api_key, cities[0], time_steps, col_list + ["date_utc"])
date_range_df.set_index("date_utc", inplace=True)
date_range_df_UTC_plus_1 = date_range_df.shift(periods=+1, freq='H')
date_range_df_UTC_plus_1.reset_index(inplace=True)
date_range_df_UTC_plus_1.rename(columns={"date_utc": "date_utc+1"}, inplace=True)

# Monats und Stunden Spalte hinzufügen
date_range_df_UTC_plus_1["month"] = date_range_df_UTC_plus_1["date_utc+1"].map(lambda x: x.month)
date_range_df_UTC_plus_1["hour"] = date_range_df_UTC_plus_1["date_utc+1"].map(lambda x: x.hour)

weather_forecast["month"] = date_range_df_UTC_plus_1["month"]
weather_forecast["hour"] = date_range_df_UTC_plus_1["hour"]

# Wetter Dataframe mit Werten aus allen Städen für das ML Model zusammenführen
for city in cities:
    weather_forecast_temp = get_forecast(api_key, city, time_steps, col_list)
    weather_forecast_temp.columns = [cities_prefix[city] + str(col) for col in weather_forecast_temp.columns]
    weather_forecast = pd.concat([weather_forecast, weather_forecast_temp], axis=1)

# Forecast mittels ML Model erstellen
wind_forecast = clf_wind.predict(weather_forecast)
#%%
# Results
wind_results = pd.DataFrame(date_range_df_UTC_plus_1["date_utc+1"])
wind_results["time (h)"] = wind_results["date_utc+1"].dt.strftime('%m-%d %H:%M')
wind_results["Wind_forecast[MWh]"] = wind_forecast

#%% Grafik der Windvorhersage erstellen
sns.set_theme()
fig1, ax1 = plt.subplots(figsize=(12, 4))
sns.barplot(data=wind_results, x="time (h)", y="Wind_forecast[MWh]")
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.show()

