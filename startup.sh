#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Make database migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# start server locally
python manage.py runserver

# Start the Gunicorn server
gunicorn --bind 0.0.0.0:8000 ptpi.wsgi:application