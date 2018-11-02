#!/bin/bash

function forzarCanal() {
    ifconfig $IWIRELESS down
    iwconfig $IWIRELESS mode monitor
    ifconfig $IWIRELESS up
    iwconfig $IWIRELESS channel $CHANNEL
}


echo "Iniciando AP"

[[ "$ALUMNSMACS" ]] && echo "$ALUMNSMACS" > /tmp/macs.txt

echo "Lanzando servicio de nombres..."
./runServicioIP.sh &
pidIP=$!


if [ ! $RESTRICTEDMODE ]; then
    if [ $FORCECHANNEL ]; then
	forzarCanal
	create_ap -c $CHANNEL "$IWIRELESS" "$IINTERNET" "$ESSID" "$PASS";
	exit 0;
    fi
    create_ap  "$IWIRELESS" "$IINTERNET" "$ESSID" "$PASS";
    exit 0;
fi

iptables -F
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

if [ $WHITEURLS ]; then
    echo "Creando reglas whitelist";
    echo "$WHITEURLS" > /tmp/whiteList.txt;
    python -u ./obtenerIPs.py /tmp/whiteList.txt > /tmp/reglas || { echo "No se pudo establecer whitelist"; exit 1; }
    . /tmp/reglas
fi

iptables -A FORWARD -d 192.168.12.1  -j ACCEPT
iptables -A FORWARD -s 192.168.12.1  -j ACCEPT
iptables -A FORWARD -j REJECT

#forzar trabajo en channel 1
#cuidado, algunos adaptadores no se vuelven a encender
if [ $FORCECHANNEL ]; then
    forzarCanal
fi

# lanzar servicio de obtencion de nombres por IP


if [ $RESTRICTMAC ]; then
    echo "Bloquear por MAC";
    for entrada in $(cat "/tmp/macs.txt"); do
	echo ${entrada%,*} >> /tmp/macsLimpias.txt
    done
    create_ap --mac-filter --mac-filter-accept /tmp/macsLimpias.txt -c $CHANNEL  $IWIRELESS lo "$ESSID" "$PASS" --isolate-clients --dhcp-dns 192.168.12.1			

else
    create_ap   -c $CHANNEL $IWIRELESS lo "$ESSID" "$PASS" --isolate-clients --dhcp-dns 192.168.12.1
fi

echo "Haciendo limpieza de firewall";



iptables -F
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

echo "Matando servicio de nombres";
kill $pidIP
