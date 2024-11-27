import time
import requests


base_url_weather = "https://api.open-meteo.com/v1/"
base_url_geo = "https://geocoding-api.open-meteo.com/v1/"


def main_weather(city):

    def get_city():
        
        url = f"{base_url_geo}search?name={city}&count=1"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            return data
        else:
            print("API FAILED")



    def get_latitude():
        latitude = get_city()['results'][0]['latitude']
        return latitude

    def get_longitude():
        longitude = get_city()['results'][0]['longitude']
        return longitude



    def get_weather_info():
        latitude = get_latitude()
        longtitude = get_longitude()
        time_interval = "hourly"
        temp = "temperature_2m"

        url = f"{base_url_weather}forecast?latitude={latitude}&longitude={longtitude}&{time_interval}={temp}"
        response = requests.get(url)
        

        if response.status_code == 200:
            weather_forecast = response.json()

            return weather_forecast
        else:
            print("DEBUG: FAILED")

    response = get_weather_info()

    return response
