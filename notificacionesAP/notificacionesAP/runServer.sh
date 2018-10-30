#!/bin/bash

python -u manage.py migrate
python -u manage.py runserver "$1":"$2"
