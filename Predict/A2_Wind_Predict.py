#%%
from Weather_And_Generation.Weather_Data_Call import ForecastWeather
from Predict.constants import TIME_STEPS_PREDICT, COL_LIST_WEATHER_PREDICT, CITY_LIST, CITIES_PREFIX

import pandas as pd
from joblib import load
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
#%%
def wind_predict():
    # Wind ML Model einlesen -> Path(__file__).parent verwenden um Datei mit dieser Funktion auch von anderer Ebene laden zu können.
    base_path = Path(__file__).parent
    file_path = (base_path / "../data/wind_model.joblib").resolve()
    clf_wind = load(file_path)

    # Weather Dataframe initialisieren
    weather_forecast = pd.DataFrame()

    # Datumsbereich bekommen, in Monat und Stunde aufteilen und als erste beiden Spalten definieren
    date_range_df = ForecastWeather(CITY_LIST[0], COL_LIST_WEATHER_PREDICT + ["date_utc"], TIME_STEPS_PREDICT).get_weather_data_for_ML_model()
    date_range_df.set_index("date_utc", inplace=True)
    date_range_df_UTC_plus_1 = date_range_df.shift(periods=+1, freq='H')
    date_range_df_UTC_plus_1.reset_index(inplace=True)
    date_range_df_UTC_plus_1.rename(columns={"date_utc": "date_utc+1"}, inplace=True)

    # Monats und Stunden Spalte hinzufügen
    date_range_df_UTC_plus_1["month"] = date_range_df_UTC_plus_1["date_utc+1"].map(lambda x: x.month)
    date_range_df_UTC_plus_1["hour"] = date_range_df_UTC_plus_1["date_utc+1"].map(lambda x: x.hour)

    weather_forecast["month"] = date_range_df_UTC_plus_1["month"]
    weather_forecast["hour"] = date_range_df_UTC_plus_1["hour"]

    # Wetter Dataframe mit Werten aus allen Städen für das ML Model zusammenführen
    for city in CITY_LIST:
        weather_forecast_temp = ForecastWeather(city, COL_LIST_WEATHER_PREDICT, TIME_STEPS_PREDICT).get_weather_data_for_ML_model()
        weather_forecast_temp.columns = [CITIES_PREFIX[city] + str(col) for col in weather_forecast_temp.columns]
        weather_forecast = pd.concat([weather_forecast, weather_forecast_temp], axis=1)

    # Forecast mittels ML Model erstellen
    wind_forecast = clf_wind.predict(weather_forecast)
    #%%
    # Results
    wind_results = pd.DataFrame(date_range_df_UTC_plus_1["date_utc+1"])
    wind_results["time (h)"] = wind_results["date_utc+1"].dt.strftime('%m-%d %H:%M')
    wind_results["Wind_forecast[MWh]"] = wind_forecast

    #%% Grafik der Windvorhersage erstellen
    sns.set_theme()
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(data=wind_results, x="time (h)", y="Wind_forecast[MWh]", palette="crest")
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.show()

    #%% Grafik speichern mit aktueller Stunde im Dateinamen
    now = datetime.now()
    time_stamp = now.strftime("%d_%m_%Hh")
    save_path = (base_path / f"../img/Windvorhersage_{time_stamp}.png").resolve()
    plt.savefig(save_path)

if __name__ == "__main__":
    wind_predict()
