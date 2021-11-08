from Weather_And_Generation.constants import STUTTGART, FREIBURG, MANNHEIM, RAVENSBURG

TIME_STEPS_PREDICT = 48

# Spaltenliste welche die jeweiligen Spalten in den History und Forecast Dataframes letztendlich darstellt
COL_LIST_WEATHER_PREDICT = ['main.temp', 'main.feels_like', 'main.pressure', 'main.humidity',
                            'wind.speed', 'wind.deg',
                            'clouds.all',
                            'weather.main']

# Städeliste
CITY_LIST = [STUTTGART, FREIBURG, MANNHEIM, RAVENSBURG]
CITIES_PREFIX = {STUTTGART: "STG_", FREIBURG: "FRB_", MANNHEIM: "MAN_", RAVENSBURG: "RAV_"}
