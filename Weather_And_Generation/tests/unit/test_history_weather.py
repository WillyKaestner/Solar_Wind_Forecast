import pytest
import pandas as pd
from datetime import datetime

from Weather_And_Generation.Weather_Data_Call import HistoryWeather

import time
from Weather_And_Generation.constants import COL_LIST, STUTTGART


@pytest.fixture()
def sample_dataframe():
    sample_data = {"unix_date": [1641812400, 1625517135],
                   "ref": ["a", "b"]}
    df = pd.DataFrame(data=sample_data)
    return df


# Testing ohne Mocks
def test_unix_to_datetime_utc():
    # sample dataframe
    sample_data = {"dt": [1641812400, 1625517135],
                   "ref": ["value_a", "value_b"]}
    df_input = pd.DataFrame(data=sample_data)

    # STG Sample Wetter Objekt
    month_in_seconds = 60 * 60 * 24 * 31
    STG = HistoryWeather(city=STUTTGART,
                         df_columns=COL_LIST,
                         start=int(time.time()) - month_in_seconds,
                         timesteps=168)

    # Methode anwenden und testen
    STG.convert_unix_to_datetime_utc(df_input)
    assert df_input.at[0, "date_utc"] == datetime.strptime("2022-01-10 11:00:00", "%Y-%m-%d %H:%M:%S")
    assert df_input.at[1, "date_utc"] == datetime.strptime("2021-07-05 20:32:15", "%Y-%m-%d %H:%M:%S")
