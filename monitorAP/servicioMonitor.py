# Servicio que mantiene una lista de personas conectadas y monitoriza cambios de conexión

import socket
import multiprocessing
import subprocess
import re
import datetime
import sys
import time
import urllib.request as rq
from urllib.error import HTTPError
import urllib.parse as parse

def iwScan(interface='wlo1'):
    while True:
        salida = subprocess.Popen(['iw', 'dev', interface, 'station', 'dump'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        texto, error = salida.communicate() # solo stdout
        if not error:
            return texto.decode('utf-8')

def filtrarMacsIw(texto):
    return re.findall('[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}', texto)

def getArpaInfo(interface='ap0'):
    comando = 'arp -an -i %s' % interface
    entradas = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    if entradas.startswith('arp:'): #las invalidas empiezan asi
        return []
    return entradas.split('\n')[:-1]

def getIPMacsConectados(interface='ap0'):
    clientes = getArpaInfo(interface)
    aux = []
    #obtener macs e IPs
    for c in clientes:
        if c:
            partes = c.split()
            aux.append((partes[3].strip(), partes[1].strip()[1:-1]))
    return aux

def ipsIw(interface='wlo1'):
    scans = iwScan(interface)
    macsConectadas = filtrarMacsIw(scans)
    macsIps = getIPMacsConectados(interface)
    dMacs = dict(macsIps)
    resultado = []
    for mac in macsConectadas:
        if mac in dMacs:
            resultado.append(dMacs[mac])
    return set(resultado)

class Monitor(multiprocessing.Process):
    def __init__(self, interface, servicioNombreHost='localhost', servicioNombrePort=9031, urlServicioNotificacion='http://localhost:8000', interval=3):
        self.interval = interval
        self.servicioNombreHost = servicioNombreHost
        self.servicioNombrePort = servicioNombrePort
        self.urlServicioNotificacion = urlServicioNotificacion
        self.interface = interface
        multiprocessing.Process.__init__(self)

    def imprimirConectados(self, ipsNombres, conectados):
        cuerpo = """
***********************
* Clientes conectados *
***********************
Hora:         %s
Numero de clientes: %s
-----------------------
%s
#######################

"""
        fecha = datetime.datetime.now()
        hora =  '%s:%s:%s' % (fecha.hour, fecha.minute, fecha.second)
        nClientes = len(conectados)
        cons = ''
        for cliente in conectados:
            cons += ipsNombres[cliente] + '\n'
        print(cuerpo % (hora, nClientes, cons))
        
    def notificar(self, mensaje):
        fecha = datetime.datetime.now()
        hora =  'Hora: %s:%s:%s\n' % (fecha.hour, fecha.minute, fecha.second)
        
        mensaje = parse.quote(hora + mensaje)

        url = '%s?mensaje=%s' % (self.urlServicioNotificacion, mensaje)
        cabeceras = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        print(url)
        request = rq.Request(url, headers=cabeceras)
        try:
            respuesta = rq.urlopen(request)
            respuesta.read() # obligar feed
        except :
            print('No es posible contactar con el servicio de notificaciones')

    def pedirNombre(self, ip):
        mySocket = socket.socket()
        mySocket.connect((self.servicioNombreHost, self.servicioNombrePort))
        message = ip
        mySocket.sendall(message.encode())
        mySocket.sendall('$$$'.encode())
        data = ''
        while not data.endswith('$$$'): # read message
            chunck = mySocket.recv(1024).decode()
            data += chunck
            if not chunck: #finished
                break
        if not data:
            raise RuntimeError("No se recibió respuesta")
        nombre = data[:-3] # quitar $$$
        mySocket.close()
        return nombre
        
    def run(self):
        conocidos = set([]) # lista de IPs conocidas
        ipsNombres = dict([]) # diccionario de pares ip:nombre
        anterior = set([]) # conjunto de clientes anterior
        while True:
            time.sleep(self.interval)
            clientesSet = ipsIw(self.interface)
            for ip in clientesSet:
                if not ip in conocidos:
                    conocidos.add(ip)
                    print('Esta es la IP:', ip)
                    nombre = self.pedirNombre(ip)
                    ipsNombres[ip] = nombre
                if ip not in anterior: # recien conectado
                    self.notificar('Se conecto: %s' % ipsNombres[ip])
                    print('Se conecto: %s' % ipsNombres[ip])

            # determinar desconectados
            desconectados = anterior - clientesSet
            for ip in desconectados:
                self.notificar('Se desconecto: %s' % ipsNombres[ip])
                print('Se desconecto: %s' % ipsNombres[ip])
            anterior = clientesSet.copy() # copia
            self.imprimirConectados(ipsNombres, clientesSet)
            

if __name__ == '__main__':
    interface = sys.argv[1]
    servicioNombreHost = sys.argv[2]
    servicioNombrePort = int(sys.argv[3])
    urlServicioNotificacion = sys.argv[4]
    monitor = Monitor(interface, servicioNombreHost, servicioNombrePort, urlServicioNotificacion)
    monitor.start()
    
