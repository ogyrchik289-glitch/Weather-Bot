import requests 
from dotenv import load_dotenv
import os
load_dotenv()


class CityError(Exception):
    pass

def get_weather(city):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('API_KEY')}&units=metric&lang=ru")
        if response.status_code != 200:
            raise CityError(f"Город {city} не найден")
            
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Погода сейчас: {weather}, температура: {temp}°C"
    except requests.exceptions.ConnectionError as e:
        return f"Ошибка подключения: {e}"


def get_weather_by_hours(city, date):    
    try:    
        response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv('API_KEY')}&units=metric&lang=ru")
        if response.status_code != 200:
            raise CityError(f"Город {city} не найден")
        data = response.json()
        weather_list = []
        for item in data["list"]:
            if item["dt_txt"].startswith(date):
                weather = item["weather"][0]["description"]
                temp = item["main"]["temp"]
                feels_like = item["main"]["feels_like"]
                time = item["dt_txt"][11:16]
                weather_list.append(f"{time}: {weather}, температура: {temp}°C, ощущается как: {feels_like}°C")      
        if not weather_list:
            return f"Погода по часам для города {city} на дату {date} не найдена, поробуйте другую дату"
        return "\n".join(weather_list)
    except requests.exceptions.ConnectionError as e:
        return f"Ошибка подключения: {e}"    

def get_weather_by_days(city, date):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv('API_KEY')}&units=metric&lang=ru")
        if response.status_code != 200:
            raise CityError(f"Город {city} не найден")
        data = response.json()
        weather_dict = {}
        for item in data["list"]:
            if item["dt_txt"][:10] == date:
                if date not in weather_dict:
                    weather_dict[date] = [item["main"]["temp"]]
                else:
                    weather_dict.get(date).append(item["main"]["temp"])
        mid_temp = sum(weather_dict[date]) / len(weather_dict[date])
        max_temp = max(weather_dict[date])
        min_temp = min(weather_dict[date])
        return f"Погода по дням для города {city} на дату {date}:\nСредняя температура: {mid_temp:.2f}°C\nМаксимальная температура: {max_temp:.2f}°C\nМинимальная температура: {min_temp:.2f}°C"
    except requests.exceptions.ConnectionError as e:    
        return f"Ошибка подключения: {e}"
            
            
            
    

