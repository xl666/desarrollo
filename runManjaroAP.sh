#!/bin/bash

cd manjaroAP/

function modoUso() {
    echo "runManjaroAP [OPCIONES] iwireless iinternet essid pass";
    echo "OPCIONES:"
    echo "   -r: Modo restringido, no se pueden comunicar los clientes ni pueden abrir páginas"
    echo "   -m archivo: archivo de macs de alumnos, formato por línea: mac,alumno"
    echo "   -w archivo: archivo de páginas whitelist una url completa por línea"
    echo "   -b: aplicar bloqueo por MAC para sólo aceptar clientes conocidos"
    echo "   -c: canal sobre el que trabaja el AP"
    echo "   -f: forzar la configuración de canal"
    echo "   -p: puerto servicio nombres desde IP"
    echo "iwireless: interfaz de red donde está el AP"
    echo "iinternte: interfaz de red que tiene internet"
    echo "essid: nombre de la red del AP"
    echo "pass: password de la red"
}

opcionR=""
opcionM=""
paramM=""
opcionW=""
paramW=""
opcionB=""
opcionC=""
paramC=1
opcionF=""
paramP="9031"
opcionP=""

while getopts ":rm:w:bc:fp:" opt; do
    case $opt in
	r)
	    opcionR="true"
	    ;;
	b)
	    opcionB="true"
	    ;;
	m)
	    opcionM="true"
	    paramM="$OPTARG"
	    ;;
	p)
	    opcionP="true"
	    paramP="$OPTARG"
	    ;;
	w)
	    opcionW="true"
	    paramW="$OPTARG"
	    ;;
	c)
	    opcionC="true"
	    paramC="$OPTARG"
	    ;;
	f)
	    opcionF="true"
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

[[ $4 ]] || { echo "número incorrecto de params"; modoUso; exit 1; }

[[ $opcionM ]] && paramM="$(cat $paramM)"
[[ $opcionW ]] && paramW="$(cat $paramW)"

docker run --rm -d -t  --net=host --name manjarotest -e IWIRELESS="$1" -e IINTERNET=$2 -e ESSID=$3 -e PASS=$4 -e RESTRICTEDMODE="$opcionR" -e WHITEURLS="$paramW" -e ALUMNSMACS="$paramM" -e IPSERVICEPORT=$paramP -e CHANNEL="$paramC" -e FORCECHANNEL=$opcionF -e RESTRICTMAC=$opcionB   --privileged  manjaroap-test


docker logs -f manjarotest
