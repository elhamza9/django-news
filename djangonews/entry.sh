#!/bin/bash

sleep 5 && \
python3 manage.py migrate && \
gunicorn --access-logfile - --log-file - --workers 2 djangonews.wsgi:application -b 0.0.0.0:8000