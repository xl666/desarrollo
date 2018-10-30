#!/bin/bash

function modoUso() {
    echo "stopManjaroAP iwireless"
    echo "iwireless: interfaz de red donde está el AP"
}

[[ $1 ]] || { modoUso; exit 1; }

docker exec manjarotest /bin/bash -c "create_ap --stop $1"
