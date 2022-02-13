import pandas as pd

from Weather_And_Generation.Weather_Data_Call import HistoryWeather
from Weather_And_Generation.constants import COL_LIST

def test_constructor(history_data_mannheim):
    assert isinstance(history_data_mannheim, HistoryWeather)

def test_data_call_from_api(history_data_mannheim):
    data = history_data_mannheim.api_call_weather_data()
    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] == history_data_mannheim.timesteps
    assert data.shape[1] >= 12

def test_confirm_sensible_data_received_from_api(history_data_mannheim):
    data = history_data_mannheim.api_call_weather_data()
    assert data["main.temp"].min() >= 250
    assert data["main.temp"].max() <= 350
    assert data["wind.speed"].min() >= 0
    assert data["wind.speed"].max() <= 50
    assert data.loc[0, "city.id"] == 2873891

def test_correct_data_columns_for_ML_input(history_data_mannheim):
    data = history_data_mannheim.get_weather_data_for_ML_model()
    assert list(data.columns) == COL_LIST

