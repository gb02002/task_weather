from geopy import Nominatim

from main.models import Stats
from datetime import datetime
import pytz


def prepare(result):
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
            for i in range(current_time_index, min(current_time_index + 5, len(times)))  # Пример для следующих 5 часов
        ],
    }

    return forecast_data


def check_new_or_add(city: str):
    # Проверка, был ли этот город уже запрашиваем
    # и добавление нового города, если он новый
    stat, created = Stats.objects.get_or_create(city=city.lower())
    if not created:
        stat.count_requests += 1
        stat.save()


