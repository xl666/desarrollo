#!/bin/bash


if [ $MONITOR ]; then
    echo "Iniciando monitor";
    echo "$ALUMNSMACS" > /tmp/macs.txt
    python -u $DIRE/monitorizarConexiones.py /tmp/macs.txt "$NOTIFICATIONSERVICE"
fi
