FROM python:3.12-slim-bullseye

LABEL authors="jay"

RUN mkdir -p /home/app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    binutils \
    libproj-dev\
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#ENV HOME=/home/web
#ENV APP_HOME=/home/orgproj/web
#RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/staticfiles
#WORKDIR $APP_HOME

# Delete build dependencies
RUN pip install --upgrade pip                                       
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./weather/entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/web/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

RUN ls -la

# copy project
COPY . .
RUN ls -la
#RUN ./entrypoint.sh
ENTRYPOINT ["/home/app/web/gunicorn.sh"]
