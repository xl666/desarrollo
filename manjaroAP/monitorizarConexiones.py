"""
Este script hace lo siguiente:

-Cuando un usuario conocido se conecta se lanza un diálogo
-Cuando un usuario desconocido se conecta dialogo
-Cuando un usuario se desconecta dialogo
-Lista continua de usuarios conectados

Requiere:

create_ap

Se debe lanzar este script despues de create_ap
"""

import subprocess
import sys
import os
import time
import datetime
import threading
import urllib.request as rq
from urllib.error import HTTPError
import urllib.parse as parse



class DialogosAsync(threading.Thread):
    """Para lanzar dialogos de sistema  asincronos
    
    """
    def __init__(self, mensaje, destino):
        hora = str(datetime.datetime.now()) + '\n'
        self.mensaje = hora + mensaje
        self.destino = destino
        threading.Thread.__init__(self)

    def run(self):
        self.mensaje = parse.quote(self.mensaje)
        url = '%s?mensaje=%s' % (self.destino, self.mensaje)
        cabeceras = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        request = rq.Request(url, headers=cabeceras)
        print(url)
        try:
            respuesta = rq.urlopen(request)
            respuesta.read() # obligar feed
        except :
            print('No es posible contactar con el servicio de notificaciones')
        
def getInfoClients(pid):
    res = []
    clientes = subprocess.Popen(['create_ap', '--list-clients', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    if not clientes.startswith('No clients connected'):
        res = clientes.split('\n')[1:] #trim headers
    return res

#regresa una version mas confiable de mac e Ip
def getArpaInfo(interface='ap0'):
    comando = 'arp -a -i %s' % interface
    entradas = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    if entradas.startswith('arp:'): #las invalidas empiezan asi
        return []
    return entradas.split('\n')[:-1]

def getMacsConectados(pid):
    clientes = getInfoClients(pid)
    aux = []
    #obtener solo macs
    for c in clientes:
        if c:
            aux.append(c.split()[0])
    return aux

def getIPMacsConectados(interface='ap0'):
    clientes = getArpaInfo(interface)
    aux = []
    #obtener macs e IPs
    for c in clientes:
        if c:
            partes = c.split()
            aux.append((partes[3].strip(), partes[1].strip()[1:-1]))
    return aux


def getNameMac(mac, users):
    for m, n in users:
        if mac == m:
            return n
    return None

def getMacIP(ip, ipMacs):
    for m, i in ipMacs:
        if i == ip:
            return m
    return None

def getNameIP(ip, ipMacs, users):
    mac = getMacIP(ip, ipMacs)
    return getNameMac(mac, users)
    

def conjuntoConectados(macs, users):
    """
    Devuelve el set resultante combinando una lista de macs con
    una lista de usuarios
    """
    res = []

    for mac in macs:
        nombre = getNameMac(mac, users)
        if nombre:
            res.append(nombre)
        else:
            res.append('Desconocido %s' % mac)
            
    return set(res)

def getUsers(pathMacs):
    users = ''
    with open(pathMacs) as macs:
        users = macs.read()

    users = users.split('\n')[:-1] #last one always empty
    #create tuple
    aux = []
    for u in users:
        aux.append(tuple(u.split(',')))
    return aux


def getPid():
    print('trata de obtner PID')
    #Obtener pid de create_ap
    instancias = subprocess.Popen(['create_ap', '--list-running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    print('se obtubo PID')
    return instancias.split('\n')[2].split()[0]


def listarActuales(actuales):
    hora = str(datetime.datetime.now())
    print('*********************')
    if actuales:
        print('Conectados %s %s' % (len(actuales), hora))
        for ac in actuales:
            print(ac)
    else:
        print('Nadie conectado %s' % hora)
    print('*********************\n')

#Obtener info de clientes conectados cada 5 segundos
def monitorizar(pid, users, servicioNotificacion):
    anteriores = set([])
    while True:
        clientes = getMacsConectados(pid)
        actuales = set([])
        if clientes:        
            actuales = conjuntoConectados(clientes, users)
            iniciando = actuales - anteriores
            saliendo = anteriores - actuales
            if iniciando:
                msj = 'Recien conectados: \n'
                for ini in iniciando:
                    msj += ini + '\n'
                hilo = DialogosAsync(msj, servicioNotificacion)
                hilo.start()

            if saliendo:
                msj = 'Se desconectaron: \n'
                for sa in saliendo:
                    msj += sa + '\n'
                hilo = DialogosAsync(msj, servicioNotificacion)
                hilo.start()

        else:
            if anteriores: #para no mandar dialogo siempre
                hilo = DialogosAsync('Se desconectaron todos', servicioNotificacion)
                hilo.start()
               
        anteriores = actuales
        listarActuales(actuales) #ver en consola
        time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Se debe especificar path the archivo con macs y servicio de notificaciones')
        exit(1)
    pathMacs = sys.argv[1]
    servicioNotificacion = sys.argv[2]
    users = getUsers(pathMacs)
    monitorizar(getPid(), users, servicioNotificacion)
