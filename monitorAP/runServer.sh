#!/bin/bash


echo "Ejecutando servidor Web"
python3 -u manage.py runserver $DOMINIO_SERVIDOR_WEB:$PUERTO_SERVIDOR_WEB & > /dev/null
SPID=$!

python3 -u servicioMonitor.py $DOMINIO_SERVICIO_NOMBRES $PUERTO_SERVICIO_NOMBRES $PUERTO $URL_SERVICIO_NOTIFICACION
echo "Termindo servidor Web..."
kill $SPID
