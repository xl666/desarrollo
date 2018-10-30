#!/bin/bash

function modoUso() {
    echo "runNotificacionesAP host puerto"
    echo "host: host donde correrá el servicio, localhost recomendado"
    echo "puerto: puerto donde correrá el servicio, 8000 recomendado"
}

[[ $2 ]] || { modoUso; exit 1; }

cd notificacionesAP/notificacionesAP/

python3 manage.py runserver $1:$2
