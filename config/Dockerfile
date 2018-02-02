FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN apt update && apt -y upgrade
RUN apt install -y libpq-dev

RUN apt-get install -y cron

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN mkdir /config
WORKDIR /config

ADD . /opt/django-favourites/
WORKDIR /opt/django-favourites/
RUN pip install --exists-action=w -r config/requirements.txt
