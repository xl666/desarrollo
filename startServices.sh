#!/bin/bash

function modoUso() {
    echo "Modo de uso:"
    echo ""
    echo "startServices.sh [OPCIONES] plantillaExamen"
    echo ""
    echo "OPCIONES:"
    echo "   -m archivo: archivo de macs de alumnos, formato por línea: mac,alumno"
    echo "   -w archivo: archivo de páginas whitelist una url completa por línea"
    echo "   -h: muestra esta ayuda"
    echo "   -i: muestra información de configuración de archivo docker-compose.yml"
    echo ""
    echo "plantillaExamen: ruta de archivo con plantilla del examen a ser aplicado"
    echo ""
    echo "El resto de la configuración puede encontrarse mediante variables establecidas en docker-compose.yml, puedes utilizar la opción -i para ver información sobre las variables importantes en docker-compose.yml"
}

opcionM=""
paramM=""
opcionW=""
paramW=""

while getopts ":m:w:h" opt; do
    case $opt in
	m)
	    opcionM="true"
	    paramM="$OPTARG"
	    ;;
	w)
	    opcionW="true"
	    paramW="$OPTARG"
	    ;;
	h)
	    modoUso
	    exit 0
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

shift $((OPTIND-1)) #borrar todos los params que ya procesó getopts

[[ $1 ]] || { echo "Se debe especificar el archivo de examen"; modoUso; exit 1; }

[[ $opcionM ]] && export MACS="$(cat $paramM)"
[[ $opcionW ]] && export WHITES="$(cat $paramW)"

cp $1 ./examenesPracticos/examenesPracticos/examen/templates/
export TEMPLATE="${1##*/}" # obtener nombre de archivo

docker-compose up
