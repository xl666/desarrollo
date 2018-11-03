#!/bin/sh

python3 -u manage.py migrate
python3 -u manage.py runserver "$1":"$2"
