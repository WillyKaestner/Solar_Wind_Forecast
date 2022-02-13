# Allgemein
API_KEY_OPENWEATHERMAP = "7660e06da8e929a654c00a31197de127"

# Spaltenliste welche die jeweiligen Spalten in den History und Forecast Dataframes letztendlich darstellt
COL_LIST = ["date_utc",
            "city.id",
            'main.temp', 'main.feels_like', 'main.pressure', 'main.humidity',
            'wind.speed', 'wind.deg',
            'clouds.all',
            'weather.main',
            'weather.description']

# Weather_history.py
START_DATE_WEATHER_HISTORY = 1601251200  # Monday, 28. September 2020 00:00:00 UTC
START_DATE_WEATHER_HISTORY_TEST = 1625443200  # Mon Jul 05 2021 00:00:00 GMT+0000
STUTTGART = "Stuttgart,DE"
FREIBURG = "Freiburg,DE"
MANNHEIM = "Mannheim,DE"
RAVENSBURG = "Ravensburg,DE"

# Smard.de
REGELZONEN = ["DE", "50Hertz", "Amperion", "TenneT", "TransnetBW"]