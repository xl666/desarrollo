#!/bin/bash

function modoUso() {
    echo "runExamenesPracticos hostServicioNombres puertoServicioNombres respuestasDir examenTemplate hostServidorWeb puertoServidorWeb"
    echo "hostServicioNombres: ip del servicio de nombres, por defecto: 192.168.12.1"
    echo "puertoServicioNombres: puerto del servicio de nombres, por defecto: 9031"
    echo "respuestasDir: directorio donde se guardaran las respuestas, debe ser una ruta relativa al directorio examenesPracticos, el directorio ya debe existir"
    echo "examenTemplate: archivo con el contenido de la pagina a mostrar, debe estar ubicado en examenesPracticos/examen/templates/, solo se pone la ruta relativa al directorio antes mencionado"
    echo "hostServidorWeb: host donde correra el servidor Web, recomendado 0.0.0.0 para que cualquier cliente tenga acceso"
    echo "puertoServidorWeb: puerto donde correrá servidor Web, recomendado 8181"
}

[[ $6 ]] || { modoUso; exit 1; }

cd examenesPracticos

python3 generarSettings.py $1 $2 $3 $4
python3 manage.py runserver $5:$6
