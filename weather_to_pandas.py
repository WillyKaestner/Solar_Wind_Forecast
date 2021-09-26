#%%
import requests
import pandas as pd

#%%
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

def get_forecast(key, city, steps, df_columns):
    # Vorhersage der Wetterdaten per API beziehen. Stündliche Werte.
    url = f"http://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={key}&cnt={steps}"
    weather_data = requests.get(url).json()

    # JSON Datei ausfächern und als Dataframe speichern
    df = pd.json_normalize(data=weather_data,
                           record_path=["list"],
                           meta=[["city", "name"], ["city", "id"]])

    # Weather ist eine Liste auf dritter Ebene, weshalb hier extra ein Dataframe erstellt wird in dem zuerst die Liste explodiert wird
    # und alle Elemente der Dict als einzelne Spalten abgespeichert werden
    # -> https://python.plainenglish.io/data-extraction-parse-a-3-nested-json-object-23cb978b66ad
    df_weather_explode = df["weather"].explode("weather")
    df_weather = pd.DataFrame(df_weather_explode.apply(pd.Series))

    # Übernahme der relevanten Weather-Werte und löschen der ursprünglichen Spalte mit den verschachtelten Daten
    df["weather.main"] = df_weather["main"]
    df["weather.description"] = df_weather["description"]
    df.drop(columns=["weather"], inplace=True)

    # Convert Unix Date to Datetime(UTC)
    df["date_utc"] = pd.to_datetime(df["dt"], unit="s", origin='unix')
    df.drop(columns=["dt", "dt_txt"], inplace=True)

    # Spaltenliste anwenden
    df = df[df_columns]
    return df.copy()


def get_history(key, city, start, steps, df_columns):
    # Vorhersage der Wetterdaten per API beziehen. Stündliche Werte.
    url = f"http://history.openweathermap.org/data/2.5/history/city?q={city}&type=hour&start={start}&cnt={steps}&appid={key}"
    weather_data = requests.get(url).json()

    # JSON Datei ausfächern und als Dataframe speichern
    df = pd.json_normalize(data=weather_data,
                           record_path=["list"],
                           meta=["city_id"])

    # city_id umbenennen
    df.rename(columns={"city_id": "city.id"}, inplace=True)

    # Weather ist eine Liste auf dritter Ebene, weshalb hier extra ein Dataframe erstellt wird in dem zuerst die Liste explodiert wird
    # und alle Elemente der Dict als einzelne Spalten abgespeichert werden
    # -> https://python.plainenglish.io/data-extraction-parse-a-3-nested-json-object-23cb978b66ad
    df_weather_explode = df["weather"].explode("weather")
    df_weather = pd.DataFrame(df_weather_explode.apply(pd.Series))

    # Übernahme der relevanten Weather-Werte und löschen der ursprünglichen Spalte mit den verschachtelten Daten
    df["weather.main"] = df_weather["main"]
    df["weather.description"] = df_weather["description"]
    df.drop(columns=["weather"], inplace=True)

    # Convert Unix Date to Datetime(UTC)
    df["date_utc"] = pd.to_datetime(df["dt"], unit="s", origin='unix')
    df.drop(columns=["dt"], inplace=True)
    df = df[df_columns]
    return df.copy()

#%%
if __name__ == "__main__":
    forecast_wetterdaten = get_forecast(api_key, city_name, 48, col_list)
    history_wetterdaten = pd.DataFrame()
    for x in range(0, 5):
        history_wetterdaten_week = get_history(api_key, city_name, (start_date_history + x * 604800), 168, col_list)
        history_wetterdaten = pd.concat([history_wetterdaten, history_wetterdaten_week], axis=0, ignore_index=True)
