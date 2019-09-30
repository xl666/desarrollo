#!/bin/bash

#Pasar todas la variables a un archivo env
echo DATABASE_NAME=$DATABASE_NAME > .env
echo DATABASE_USER=$DATABASE_USER >> .env
echo DATABASE_PASSWORD=$DATABASE_PASSWORD >> .env
echo DATABASE_HOST=$DATABASE_HOST >> .env
echo DATABASE_PORT=$DATABASE_PORT >> .env


python -u manage.py makemigrations 
python -u manage.py migrate

gunicorn --bind :8000 examenesEscritos.wsgi:application --reload
