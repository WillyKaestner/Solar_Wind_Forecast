import time
import pytest

from Weather_And_Generation.Weather_Data_Call import HistoryWeather
from Weather_And_Generation.constants import COL_LIST, STUTTGART, MANNHEIM


@pytest.fixture()
def history_data_stuttgart():
    month_in_seconds = 60*60*24*31
    return HistoryWeather(city=STUTTGART,
                          df_columns=COL_LIST,
                          start=int(time.time()) - month_in_seconds,
                          timesteps=168)

@pytest.fixture()
def history_data_mannheim():
    month_in_seconds = 60*60*24*31
    return HistoryWeather(city=MANNHEIM,
                          df_columns=COL_LIST,
                          start=int(time.time()) - month_in_seconds,
                          timesteps=168)
