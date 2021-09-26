#%%
import requests
import pandas as pd
import numpy as np
import json

#%%
city_name = "Seattle,US"
api_key = "7660e06da8e929a654c00a31197de127"

def get_weather(key, city):
    url = f"http://pro.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    response = requests.get(url).json()

    temp = response["main"]["temp"]
    temp = np.round(temp - 273.15)  # Kelvin zu °C

    feels_like = response["main"]["feels_like"]
    feels_like = np.round(feels_like - 273.15)  # Kelvin zu °C)

    humidity = response["main"]["humidity"]

    weather = {
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
    }
    print(weather)

def get_forecast(key, city, steps):
    url = f"http://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={key}&cnt={steps}"
    response = requests.get(url).json()
    print(response)

def save_weather_json(key, city):
    url = f"http://pro.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    response = requests.get(url)
    with open('wetter.json', 'wb') as outf:
        outf.write(response.content)

def save_forecast_json(key, city, steps):
    url = f"http://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={key}&cnt={steps}"
    response = requests.get(url)
    with open('forecast.json', 'wb') as outf:
        outf.write(response.content)


if __name__ == "__main__":
    # get_weather(api_key, city_name)

    # save_weather_json(api_key, city_name)
    save_forecast_json(api_key, city_name, 2)
