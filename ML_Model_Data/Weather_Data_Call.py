"""
Hilfsskript um die restlichen Skripte in ML_Model_Data sauber zu halten
"""
import requests
import pandas as pd

class WeatherData:
    """
    Overall weather data

    :param city: Weather location
    :param df_columns: List of columns for the final dataframe which is returned.
    """
    from ML_Model_Data.constants import API_KEY

    def __init__(self, city: str, df_columns: list):
        self.city = city
        self.df_columns = df_columns

    def prepare_dataframe_for_ML_model_use(self, df: pd.DataFrame) -> pd.DataFrame:
        """Explode hidden data in the dataframe, convert to UTC time and select given columns"""
        # Wetterbezeichnungen sind als Liste in der Spalte "weather" vergraben -> extratieren der Werte und speichern eigene Spalten
        self.create_columns_with_weather_description_data(df)
        # Convert Unix Date to Datetime(UTC)
        self.convert_unix_to_datetime_utc(df)
        # Spaltenliste anwenden
        df = df[self.df_columns]
        return df

    @staticmethod
    def create_columns_with_weather_description_data(df: pd.DataFrame):
        """Explode data in weather column of the received weather dataframe"""
        # Weather ist eine Liste auf dritter Ebene, weshalb hier extra ein Dataframe erstellt wird in dem zuerst die Liste explodiert wird
        # und alle Elemente der Dict als einzelne Spalten abgespeichert werden
        # -> https://python.plainenglish.io/data-extraction-parse-a-3-nested-json-object-23cb978b66ad
        df_weather_explode = df["weather"].explode("weather")
        df_weather = pd.DataFrame(df_weather_explode.apply(pd.Series))

        # Übernahme der relevanten Weather-Werte und löschen der ursprünglichen Spalte mit den verschachtelten Daten
        df["weather.main"] = df_weather["main"]
        df["weather.description"] = df_weather["description"]
        df.drop(columns=["weather"], inplace=True)

    @staticmethod
    def convert_unix_to_datetime_utc(df: pd.DataFrame):
        """Convert column with Unix Date to Datetime(UTC)"""
        df["date_utc"] = pd.to_datetime(df["dt"], unit="s", origin='unix')

class HistoryWeather(WeatherData):
    """
    Create HistoryWeather from BaseClass WeatherData

    :param city: Weather location
    :param df_columns: List of columns for the final dataframe which is returned.
    :param start: Start time of history values in Unix Time
    :param steps: amount of history time steps in hours
    """

    def __init__(self, city: str, df_columns: list, start: int, steps: int):
        super().__init__(city, df_columns)
        self.start = start
        self.steps = steps

    def api_call_weather_history(self) -> pd.DataFrame:
        """Historische Wetterdaten per API beziehen. Stündliche Werte."""
        url = f"https://history.openweathermap.org/data/2.5/history/city?q={self.city}&type=hour&start={self.start}&cnt={self.steps}&appid={self.API_KEY}"
        weather_data = requests.get(url).json()
        # JSON Datei ausfächern und als Dataframe speichern
        df = pd.json_normalize(data=weather_data,
                               record_path=["list"],
                               meta=["city_id"])
        # city_id umbenennen
        df.rename(columns={"city_id": "city.id"}, inplace=True)
        return df

    def get_weather_history(self) -> pd.DataFrame:
        """ Get the history Data from Openweather with a specific start time in the past and a certain amount of time steps."""
        # Laden der historischen Wetterdaten
        df = self.api_call_weather_history()
        # Wetterbezeichnung ausfächern, Datum in UTC umwandeln & Spaltenabgleich zwischen Wettervorhersage und historischen Wetterdaten gewährleisten
        df = self.prepare_dataframe_for_ML_model_use(df)
        return df


class ForecastWeather(WeatherData):
    """
    Create ForecastWeather from BaseClass WeatherData

    :param city: Weather location
    :param df_columns: List of columns for the final dataframe which is returned.
    :param steps: amount of history time steps in hours
    """

    def __init__(self, city: str, df_columns: list, steps: int):
        super().__init__(city, df_columns)
        self.steps = steps

    def api_call_weather_forecast(self) -> pd.DataFrame:
        """Vorhersage der Wetterdaten per API beziehen. Stündliche Werte."""
        url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={self.city}&appid={self.API_KEY}&cnt={self.steps}"
        weather_data = requests.get(url).json()
        # JSON Datei ausfächern und als Dataframe speichern
        df = pd.json_normalize(data=weather_data,
                               record_path=["list"],
                               meta=[["city", "name"], ["city", "id"]])
        return df

    def get_weather_forecast(self) -> pd.DataFrame:
        """Vorhersage der Wetterdaten ab der aktuellen Stunde per API beziehen. Stündliche Werte."""
        # Laden der Wettervorhersage
        df = self.api_call_weather_forecast()
        # Wetterbezeichnung ausfächern, Datum in UTC umwandeln & Spaltenabgleich zwischen Wettervorhersage und historischen Wetterdaten gewährleisten
        df = self.prepare_dataframe_for_ML_model_use(df)
        return df


# %%
from Decorators.decorators import my_timer

@my_timer
def main():
    from Predict.constants import TIME_STEPS_PREDICT, COL_LIST_WEATHER_PREDICT, CITY_LIST
    from ML_Model_Data.constants import START_DATE_WEATHER_HISTORY_TEST

    weather_forecast_data_stuttgart = ForecastWeather(CITY_LIST[0], COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                      TIME_STEPS_PREDICT).get_weather_forecast()
    weather_forecast_data_freiburg = ForecastWeather(CITY_LIST[1], COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                     TIME_STEPS_PREDICT).get_weather_forecast()

    weather_history_data_stuttgart = HistoryWeather(city=CITY_LIST[0],
                                                    df_columns=COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                    start=START_DATE_WEATHER_HISTORY_TEST,
                                                    steps=10).get_weather_history()
    return weather_forecast_data_stuttgart, weather_forecast_data_freiburg, weather_history_data_stuttgart


if __name__ == "__main__":
    weather_forecast_data_stuttgart, weather_forecast_data_freiburg, weather_history_data_stuttgart = main()
