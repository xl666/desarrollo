#!/bin/bash

echo "exitooo" > /tmp/ap.txt
[[ $ALUMNSMACS ]] || exit 1
#tratar de obtener nombre ap
function nombreAP() {
    local deInter=""
    while [ ! "$deInter" ]; do
	local instancias="$(/bin/bash -c 'create_ap --list-running')"
	deInter="$(echo $instancias | grep $IWIRELESS)"
	if [ "$deInter" ]; then
	    local apAux="${deInter#*$IWIRELESS (}";
	    local ap="${apAux%)}";
	    echo $ap;
	    return
	fi
	sleep 2;
    done
}


ap=$(nombreAP)
echo "$ap" > /tmp/ap.txt
python servicioIPAlumno.py /tmp/macs.txt $ap $IPSERVICEPORT
