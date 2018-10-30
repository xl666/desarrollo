# Servicio que mantiene una lista de personas conectadas y monitoriza cambios de conexión

import socket
import multiprocessing
import subprocess
import datetime
import sys
import time
from multiprocessing import Queue
import urllib.request as rq
from urllib.error import HTTPError
import urllib.parse as parse

# vuelva en un set el contenido de un Queue compartido
def volcarCola(cola):
    res = set([])
    try:
        while(True):
            res.add(cola.get_nowait())
    except:
        pass
    return res

class Monitor(multiprocessing.Process):
    def __init__(self, clientes, lock, servicioNombreHost='localhost', servicioNombrePort=9031, urlServicioNotificacion='http://localhost:8000', interval=6):
        self.clientes = clientes
        self.interval = interval
        self.lock = lock
        self.servicioNombreHost = servicioNombreHost
        self.servicioNombrePort = servicioNombrePort
        self.urlServicioNotificacion = urlServicioNotificacion
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
            self.lock.acquire()
            clientesSet = volcarCola(self.clientes)
            self.lock.release()
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
            
class Servicio():
    def __init__(self, clientes, lock, port=9131):        
        self.port = port
        self.lock = lock
        self.clientes = clientes # conjunto que se va a sincronizar
        
    def run(self):
        """
        crear socket de servicio
        """
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind(('', int(self.port)))  # binds to any available interface
        print('recibiendo peticiones en puerto: %s' % self.port)
        mySocket.listen(20)
        while True:
            conn, addr = mySocket.accept()
            attendThread = WorkThread(conn, addr, self.lock, self.clientes) # se crea un hilo de atención por cliente
            attendThread.start()

            
class WorkThread(multiprocessing.Process):  # it is actually a subprocess
    def __init__(self, conn, addr, lock, clientes):
        self.conn = conn
        self.addr = addr
        self.lock = lock
        self.clientes = clientes        
        multiprocessing.Process.__init__(self)

    def run(self):
        data = ''
        # Se recibe 1 cosa en la serializacion: IP
        # El final de la cadena es $$$
        while not data.endswith('$$$'): # read message
            chunck = self.conn.recv(1024).decode()
            data += chunck
            if not chunck: #finished
                break
        if not data:
            raise RuntimeError("No se transmitieron datos")
            self.conn.sendall("('API error', 1)$$$".encode())
            return
        data = data[:-3] # quitar $$$
        ip = data.strip()
        
        self.lock.acquire()
        self.clientes.put(ip)
        self.lock.release()
        
        self.conn.close()


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    clientes = Queue()
    servicioNombreHost = sys.argv[1]
    servicioNombrePort = int(sys.argv[2])
    urlServicioNotificacion = sys.argv[4]
    monitor = Monitor(clientes, lock, servicioNombreHost, servicioNombrePort, urlServicioNotificacion)
    monitor.start()
    puerto = int(sys.argv[3])
    servicio = Servicio(clientes, lock, puerto)
    servicio.run()
    
