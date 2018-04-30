#!/bin/bash

sleep 5 # quick fix to wait for DB to start
python3 manage.py migrate
python3 manage.py collectstatic --noinput
