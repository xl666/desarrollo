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

def arpScan(interface='wlo1', dominio='192.168.12.0/24'):
    while True:
        salida = subprocess.Popen(['arp-scan', '--interface=%s' % interface, '--retry=3',dominio], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        texto, error = salida.communicate() # solo stdout
        if not error:
            return texto.decode('utf-8')

def filtrarIpsARP(texto):
    return re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', texto)

def ipsARP(interface='wlo1', dominio='192.168.12.0/24'):
    texto = arpScan(interface, dominio)
    return set(filtrarIpsARP(texto))

class Monitor(multiprocessing.Process):
    def __init__(self, interface, dominio, servicioNombreHost='localhost', servicioNombrePort=9031, urlServicioNotificacion='http://localhost:8000', interval=3):
        self.interval = interval
        self.servicioNombreHost = servicioNombreHost
        self.servicioNombrePort = servicioNombrePort
        self.urlServicioNotificacion = urlServicioNotificacion
        self.interface = interface
        self.dominio = dominio
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
            clientesSet = ipsARP(self.interface, self.dominio)
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
    dominio = sys.argv[2]
    servicioNombreHost = sys.argv[3]
    servicioNombrePort = int(sys.argv[4])
    urlServicioNotificacion = sys.argv[5]
    monitor = Monitor(interface, dominio, servicioNombreHost, servicioNombrePort, urlServicioNotificacion)
    monitor.start()
    
