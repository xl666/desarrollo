#!/bin/bash

docker exec -t -i examenesEscritos bash -c 'python manage.py createsuperuser' && echo "Administrador creado con éxito" || { echo "Hubo un error al crear al usuario administrador"; exit 1; }
