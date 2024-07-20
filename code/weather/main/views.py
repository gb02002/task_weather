import os
from datetime import datetime

import pytz
from django.shortcuts import render
from django.views import View
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
from rest_framework.generics import get_object_or_404

from main.models import Stats
import requests

from main.utils import prepare, check_new_or_add

# Create your views here.
PARSING_URL = os.getenv("URL", 'https://api.open-meteo.com/v1/forecast')


# class StartWeatherView(View):
#     template_name = 'weather.html'  # Укажите шаблон для отображения результата
#
#     # def get(self, request):
#     #     city = request.GET.get('city')  # Извлечение города из параметров запроса
#     #     if city:
#     #         try:
#     #             coords = get_coords(city)
#     #             response = requests.get(PARSING_URL, params={
#     #                     "latitude": coords[0],
#     #                     "longitude": coords[1],
#     #                     "hourly": "temperature_2m"
#     #                 }).json()
#     #
#     #             if response:
#     #                 prepared_result = prepare(response)
#     #                 check_new_or_add(city)  # Проверка и добавление города
#     #                 return render(request, self.template_name, {'city': city, 'result': prepared_result})
#     #
#     #             return render(request, self.template_name, {'message': "No content available for this city"})
#     #         except Exception as e:
#     #             print(f"Error fetching weather data: {e}")
#     #             return render(request, self.template_name, {'error': str(e)})
#     #     return render(request, self.template_name, {'message': "City not specified"})
#
#     def get(self, request, city=None):
#         city = request.GET.get('city')
#         if city:
#             try:
#                 latitude, longitude = get_coords(city)
#                 if latitude and longitude:
#                     weather_url = "https://api.open-meteo.com/v1/forecast"
#                     params = {
#                         "latitude": latitude,
#                         "longitude": longitude,
#                         "hourly": "temperature_2m"
#                     }
#                     response = requests.get(weather_url, params=params).json()
#                     if response:
#                         prepared_result = prepare(response)
#
#                         # Сохранени е последнего запрашиваемого города в сессии
#                         request.session['last_city'] = city
#
#                         return render(request, self.template_name, {'city': city, 'result': prepared_result})
#                 return render(request, self.template_name,
#                               {'city': city, 'message': "Could not find coordinates for the specified city"})
#             except Exception as e:
#                 print(f"Error: {e}")
#                 return render(request, self.template_name, {'city': city, 'error': str(e)})
#
#         # Если нет города в запросе, показываем последний запрашиваемый город из сессии
#         else:
#             last_city = request.session.get('last_city')
#             if last_city:
#                 self.get(request, last_city)
#                 # return render(request, self.template_name, {'city': last_city, 'message': "Showing last searched city"})
#             return render(request, self.template_name)


class StartWeatherView(View):
    template_name = 'weather.html'

    @staticmethod
    def get_coordinates(city: str) -> tuple:
        geolocator = Nominatim(user_agent="my_unique_application_name")
        try:
            location = geolocator.geocode(city, timeout=10)  # Увеличьте таймаут, если нужно
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderTimedOut:
            print(f"Geocoder service timed out for city: {city}")
            return None, None
        except GeocoderInsufficientPrivileges:
            print("Apparently you reached top requests to api")
            return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None

    @staticmethod
    def fetch_weather_data(latitude, longitude):
        # Метод для получения данных о погоде
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        response = requests.get(weather_url, params=params).json()
        return response

    @staticmethod
    def prepare_result(result):
        # Получаем текущее время по временной зоне, указанной в данных
        timezone = result.get('timezone', 'UTC')
        utc_now = datetime.now(pytz.utc)
        local_now = utc_now.astimezone(pytz.timezone(timezone))

        # Извлекаем данные о времени и температуре
        times = result['hourly']['time']
        temperatures = result['hourly']['temperature_2m']

        # Поиск индекса текущего времени
        current_time_index = next((i for i, t in enumerate(times) if t >= local_now.isoformat()), None)
        if current_time_index is None:
            current_time_index = 0  # Если текущее время не найдено, берем первое доступное время

        # Подготовка данных для отображения
        forecast_data = {
            'current_time': times[current_time_index],
            'current_temperature': temperatures[current_time_index],
            'hourly_forecast': [
                {'time': times[i], 'temperature': temperatures[i]}
                for i in range(current_time_index, min(current_time_index + 5, len(times)))
                # Пример для следующих 5 часов
            ],
        }

        return forecast_data

    def get(self, request, city=None):
        if request.GET.get('city'):
            check_new_or_add(request.GET.get('city'))
        city = request.GET.get('city') or city
        if city:
            try:
                latitude, longitude = self.get_coordinates(city)
                if latitude and longitude:
                    weather_data = self.fetch_weather_data(latitude, longitude)
                    if weather_data:
                        prepared_result = self.prepare_result(weather_data)

                        # Сохранение последнего запрашиваемого города в сессии
                        request.session['last_city'] = city

                        return render(request, self.template_name, {'city': city, 'result': prepared_result})
                return render(request, self.template_name,
                              {'city': city, 'message': "Could not find coordinates for the specified city"})
            except Exception as e:
                print(f"Error: {e}")
                return render(request, self.template_name, {'city': city, 'error': str(e)})
        else:
            last_city = request.session.get('last_city')
            if last_city:
                return self.get(request, last_city)  # Рекурсивный вызов для последнего города

        # Если нет города и в сессии нет последнего города
        return render(request, self.template_name,
                      {'message': "No city provided. Please enter a city to get the weather forecast."})


def request_stats(request, city):
    query = get_object_or_404(Stats, city=city)
    return render(request, 'stat.html', {'city': query.city, 'request_count': query.count_requests})
