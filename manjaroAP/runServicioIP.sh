#!/bin/bash

echo "exitooo" > /tmp/ap.txt
[[ $ALUMNSMACS ]] || exit 1 #no tiene sentido lanzar servicio sin macs
#tratar de obtener nombre ap
function nombreAP() {
    local deInter=""
    while [ ! "$deInter" ]; do
	local instancias="$(/bin/bash -c 'create_ap --list-running')"
	deInter="$(echo $instancias | grep $IWIRELESS)"
	if [ "$deInter" ]; then
	    parentesis="$(echo $deInter | grep '(')" #no se soportan interfaces virtuales
	    if [ ! "$parentesis" ]; then
		local ap=$IWIRELESS
		echo $IWIRELESS
		return
	    else
		local apAux="${deInter#*$IWIRELESS (}";
		local ap="${apAux%)}";
		echo $ap;
		return
	    fi
	fi
	sleep 2;
    done
}


ap=$(nombreAP)
echo "$ap" > /tmp/ap.txt
python -u servicioIPAlumno.py /tmp/macs.txt $ap $IPSERVICEPORT
