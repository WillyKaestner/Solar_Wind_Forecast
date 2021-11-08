"""
Weather data classes and functions to load and prepare weather data for further use
"""
import requests
import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class WeatherData(ABC):
    """Overall weather data"""
    from Weather_And_Generation.constants import API_KEY_OPENWEATHERMAP
    city: str           # Weather location
    df_columns: list    # List of columns for the final dataframe which is returned.

    @abstractmethod
    def api_call_weather_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def read_weather_data_from_file(self) -> pd.DataFrame:
        pass

    def get_weather_data_for_ML_model(self) -> pd.DataFrame:
        """Wetterdaten per API beziehen"""
        # Laden der wetter daten
        df = self.api_call_weather_data()
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

@dataclass
class HistoryWeather(WeatherData):
    """Create HistoryWeather from BaseClass WeatherData"""
    start: int          # Start time of history values in Unix Time
    timesteps: int = 168    # amount of history time steps in hours

    def api_call_weather_data(self) -> pd.DataFrame:
        """Historische Wetterdaten per API beziehen. Stündliche Werte."""
        url = f"https://history.openweathermap.org/data/2.5/history/city?q={self.city}&type=hour&start={self.start}&cnt={self.timesteps}&appid={self.API_KEY_OPENWEATHERMAP}"
        weather_data = requests.get(url).json()
        # JSON Datei ausfächern und als Dataframe speichern
        df = pd.json_normalize(data=weather_data,
                               record_path=["list"],
                               meta=["city_id"])
        # city_id umbenennen
        df.rename(columns={"city_id": "city.id"}, inplace=True)
        return df

    def read_weather_data_from_file(self) -> pd.DataFrame:
        pass

@dataclass
class ForecastWeather(WeatherData):
    """Create ForecastWeather from BaseClass WeatherData"""
    timesteps: int = 48     # amount of forecast time steps in hours

    def api_call_weather_data(self) -> pd.DataFrame:
        """Vorhersage der Wetterdaten per API beziehen. Stündliche Werte."""
        url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={self.city}&appid={self.API_KEY_OPENWEATHERMAP}&cnt={self.timesteps}"
        weather_data = requests.get(url).json()
        # JSON Datei ausfächern und als Dataframe speichern
        df = pd.json_normalize(data=weather_data,
                               record_path=["list"],
                               meta=[["city", "name"], ["city", "id"]])
        return df

    def read_weather_data_from_file(self) -> pd.DataFrame:
        pass


# %%
from Decorators.decorators import my_timer

@my_timer
def main():
    from Predict.constants import TIME_STEPS_PREDICT, COL_LIST_WEATHER_PREDICT, CITY_LIST
    from Weather_And_Generation.constants import START_DATE_WEATHER_HISTORY_TEST

    weather_forecast_data_stuttgart = ForecastWeather(city=CITY_LIST[0],
                                                      df_columns=COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                      timesteps=TIME_STEPS_PREDICT).get_weather_data_for_ML_model()

    weather_forecast_data_freiburg = ForecastWeather(city=CITY_LIST[1],
                                                     df_columns=COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                     timesteps=TIME_STEPS_PREDICT).get_weather_data_for_ML_model()

    weather_history_data_stuttgart = HistoryWeather(city=CITY_LIST[0],
                                                    df_columns=COL_LIST_WEATHER_PREDICT + ["date_utc"],
                                                    start=START_DATE_WEATHER_HISTORY_TEST,
                                                    timesteps=10).get_weather_data_for_ML_model()
    return weather_forecast_data_stuttgart, weather_forecast_data_freiburg, weather_history_data_stuttgart


if __name__ == "__main__":
    weather_forecast_data_stuttgart, weather_forecast_data_freiburg, weather_history_data_stuttgart = main()
