#!/bin/bash

# obtener nombre de contenedor de access point
nombreAccess=$(docker-compose ps | egrep -o ".*accesspoint[^ ]*")

if [ $nombreAccess ]; then
    # obtner nombre de access
    ap=$(docker exec $nombreAccess /bin/bash -c 'cat /tmp/ap.txt')
    # obtener pid de create_ap
    pid=$(docker exec $nombreAccess /bin/bash -c 'create_ap --list-running' | egrep $ap | egrep -o "^[0-9]+")
    # detener accesspoint de forma limpia
    docker exec $nombreAccess /bin/bash -c "create_ap --stop $pid" || { echo "Hubo un problema deteniendo el access point, no se ha detenido nada"; exit 1; }
    echo "access point detenido"
fi

docker-compose down
echo "Todos los sistemas detenidos"
