# Используем образ Python
FROM python:3.12-bullseye

LABEL authors="jay"

# Создаем рабочую директорию
WORKDIR /home/app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    binutils \
    libproj-dev \
    gdal-bin\
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем файл требований и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем скрипт для запуска приложения и устанавливаем права на выполнение

# Копируем весь проект в рабочую директорию
COPY . .

# Выполняем команду для отображения содержимого директории (для отладки)
RUN cd /home/app/weather/
RUN ls -la weather

# Запуск Django приложения через manage.py
ENTRYPOINT ["python", "weather/manage.py"]

# Запускаем сервер Django
CMD ["runserver", "0.0.0.0:8000"]
