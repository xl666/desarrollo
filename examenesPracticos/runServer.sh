#!/bin/sh

cd /code

echo "Ejecutando servicio de exámenes prácticos"

mkdir "respuestas/$DIRECTORIO_RESPUESTA" 2> /dev/null


python3 -u generarSettings.py $DOMINIO_SERVICIO_NOMBRES $PUERTO_SERVICIO_NOMBRES "respuestas/$DIRECTORIO_RESPUESTA" "$TEMPLATE_EXAMEN"
python3 -u manage.py runserver $DOMINIO_SERVIDOR_WEB:$PUERTO_SERVIDOR_WEB


