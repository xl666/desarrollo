#!/bin/bash

function modoUso() {
    echo "startServices.sh [OPCIONES]"
    echo "OPCIONES:"
    echo "   -m archivo: archivo de macs de alumnos, formato por línea: mac,alumno"
    echo "   -w archivo: archivo de páginas whitelist una url completa por línea"
    echo ""
    echo "El resto de la configuración puede encontrarse mediante variables establecidas en docker-compose.yml"
}

opcionM=""
paramM=""
opcionW=""
paramW=""

while getopts ":m:w:" opt; do
    case $opt in
	m)
	    opcionM="true"
	    paramM="$OPTARG"
	    ;;
	w)
	    opcionW="true"
	    paramW="$OPTARG"
	    ;;
	"?")
	    echo "Opción inválida -$OPTARG";
	    modoUso;
	    exit 1;
	    ;;
	:)
	    echo "Se esperaba un parámetro en -$OPTARG";
	    modoUso;
	    exit 1;
	    ;;
    esac
done

[[ $opcionM ]] && export MACS="$(cat $paramM)"
[[ $opcionW ]] && export WHITES="$(cat $paramW)"

docker-compose up
