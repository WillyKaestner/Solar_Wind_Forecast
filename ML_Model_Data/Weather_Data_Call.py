"""
Hilfsskript um die restlichen Skripte in ML_Model_Data sauber zu halten
"""
from ML_Model_Data.constants import API_KEY
import requests
import pandas as pd

"""
01 Übergreifende Funktionen zur Abfrage von historischen und zukünftigen Wetterdaten
"""

def get_weather_forecast(city: str, steps: int, df_columns: list) -> pd.DataFrame:
    """
    Vorhersage der Wetterdaten ab der aktuellen Stunde per API beziehen. Stündliche Werte.

    :param city: Weather location
    :param steps: Amount of forecasted time steps in hours
    :param df_columns: List of columns for the final dataframe which is returned. See online documentation of openweathermap for overall
    list of history weather variables
    :return: Pandas Dataframe of the weather forecast values
    """
    # Laden der Wettervorhersage
    df = api_call_weather_forecast(city, steps)

    # Wetterbezeichnung ausfächern, Datum in UTC umwandeln & Spaltenabgleich zwischen Wettervorhersage und historischen Wetterdaten gewährleisten
    df = prepare_dataframe_for_ML_model_use(df, df_columns)
    return df.copy()


def get_weather_history(city: str, start: int, steps: int, df_columns: list) -> pd.DataFrame:
    """
    Get the history Data from Openweather with a specific start time in the past and a certains amout of time steps.

    :param city: Weather location
    :param start: Start time of history values in Unix Time
    :param steps: amount of history time steps in hours
    :param df_columns: List of columns for the final dataframe which is returned. See online documentation of openweathermap for overall
    list of history weather variables
    :return: Pandas Dataframe of the weather history values
    """
    # Laden der historischen Wetterdaten
    df = api_call_weather_history(city, start, steps)

    # Wetterbezeichnung ausfächern, Datum in UTC umwandeln & Spaltenabgleich zwischen Wettervorhersage und historischen Wetterdaten gewährleisten
    df = prepare_dataframe_for_ML_model_use(df, df_columns)
    return df.copy()

"""
02 Hilfsfunktionen zur Wetterabfrage und Datenbearbeitung
"""

def api_call_weather_forecast(city: str, steps: int) -> pd.DataFrame:
    # Vorhersage der Wetterdaten per API beziehen. Stündliche Werte.
    url = f"http://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={API_KEY}&cnt={steps}"
    weather_data = requests.get(url).json()

    # JSON Datei ausfächern und als Dataframe speichern
    df = pd.json_normalize(data=weather_data,
                           record_path=["list"],
                           meta=[["city", "name"], ["city", "id"]])
    return df

def api_call_weather_history(city: str, start: int, steps: int) -> pd.DataFrame:
    # Historische Wetterdaten per API beziehen. Stündliche Werte.
    url = f"http://history.openweathermap.org/data/2.5/history/city?q={city}&type=hour&start={start}&cnt={steps}&appid={API_KEY}"
    weather_data = requests.get(url).json()

    # JSON Datei ausfächern und als Dataframe speichern
    df = pd.json_normalize(data=weather_data,
                           record_path=["list"],
                           meta=["city_id"])

    # city_id umbenennen
    df.rename(columns={"city_id": "city.id"}, inplace=True)
    return df

def create_columns_with_weather_description_data(df: pd.DataFrame):
    # Weather ist eine Liste auf dritter Ebene, weshalb hier extra ein Dataframe erstellt wird in dem zuerst die Liste explodiert wird
    # und alle Elemente der Dict als einzelne Spalten abgespeichert werden
    # -> https://python.plainenglish.io/data-extraction-parse-a-3-nested-json-object-23cb978b66ad
    df_weather_explode = df["weather"].explode("weather")
    df_weather = pd.DataFrame(df_weather_explode.apply(pd.Series))

    # Übernahme der relevanten Weather-Werte und löschen der ursprünglichen Spalte mit den verschachtelten Daten
    df["weather.main"] = df_weather["main"]
    df["weather.description"] = df_weather["description"]
    df.drop(columns=["weather"], inplace=True)

def convert_unix_to_datetime_utc(df: pd.DataFrame):
    # Convert Unix Date to Datetime(UTC)
    df["date_utc"] = pd.to_datetime(df["dt"], unit="s", origin='unix')
    # df.drop(columns=["dt", "dt_txt"], inplace=True)

def prepare_dataframe_for_ML_model_use(df: pd.DataFrame, df_columns: list) -> pd.DataFrame:
    # Wetterbezeichnungen sind als Liste in der Spalte "weather" vergraben -> extratieren der Werte und speichern eigene Spalten
    create_columns_with_weather_description_data(df)

    # Convert Unix Date to Datetime(UTC)
    convert_unix_to_datetime_utc(df)

    # Spaltenliste anwenden
    df = df[df_columns]
    return df
