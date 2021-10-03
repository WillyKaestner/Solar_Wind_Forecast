#%%
"""
Helper functions to fetch weather data from Openweathermap. Historical and forecast weather can be accessed via api.
"""
import requests
import pandas as pd
from ML_Model_Data.constants import API_KEY, FREIBURG, STUTTGART, COL_LIST, START_DATE_WEATHER_HISTORY

#%%
def get_forecast(key, city, steps, df_columns):
    """
    Get the forecast Data from Openweather beginning with the current hour.

    :param key: Personal Api Key
    :param city: Weather location
    :param steps: amount of forecasted time steps in hours
    :param df_columns: List of columns for the final dataframe which is returned. See online documentation of openweathermap for overall
    list of forecast weather variables
    :return: Pandas Dataframe of the weather forecast values
    """
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
    """
    Get the history Data from Openweather with a specific start time in the past and a certains amout of time steps.

    :param key: Personal Api Key
    :param city: Weather location
    :param start: Start time of history values in Unix Time
    :param steps: amount of history time steps in hours
    :param df_columns: List of columns for the final dataframe which is returned. See online documentation of openweathermap for overall
    list of history weather variables
    :return: Pandas Dataframe of the weather history values
    """
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
    forecast_wetterdaten = get_forecast(API_KEY, FREIBURG, 48, COL_LIST)

