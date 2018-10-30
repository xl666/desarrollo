#!/bin/bash

function modoUso() {
    echo "startMonitorAP hostServicioNombres puertoServicioNombres puerto urlServicioNotificacion hostServidorWeb puertoServidorWeb"
    echo "hostServicioNombres: ip del servicio de nombres, por defecto: 192.168.12.1"
    echo "puertoServicioNombres: puerto del servicio de nombres, por defecto: 9031 "
    echo "puerto: puerto servicio interno, por defecto: 9131"
    echo "urlServicioNotificacion: url del servicio de notificaciones, por ejemplo: http://localhost:8000/guardarMensaje"
    echo "hostServidorWeb: host donde correra el servidor Web, recomendado 0.0.0.0 para que cualquier cliente tenga acceso"
    echo "puertoServidorWeb: puerto donde correrá servidor Web, recomendado 9595"
}

[[ $6 ]] || { modoUso; exit 1; }

cd monitorAP/monitorAP/
echo "Ejecutando servidor Web"
python3 manage.py runserver $5:$6 & > /dev/null
cd ..
python3 servicioMonitor.py $1 $2 $3 $4
echo "Termindo servidor Web..."
kill $!
