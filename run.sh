#!/bin/bash

python manage.py migrate && \
    python manage.py loaddata favourites/zoo/fixtures/koko.json && \
    python manage.py runserver 0.0.0.0:8000
