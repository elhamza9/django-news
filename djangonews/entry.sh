#!/bin/bash

sleep 5 # quick fix to wait for DB to start
python3 manage.py migrate
python3 manage.py collectstatic
gunicorn --access-logfile - --log-file - --workers 2 djangonews.wsgi:application -b 0.0.0.0:8000
