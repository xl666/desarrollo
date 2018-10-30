# Este servicio recibe una IP y regresa el nombre del alumno asociado


import subprocess
import socket
import multiprocessing
import sys

def getPid():
    #Obtener pid de create_ap
    instancias = subprocess.Popen(['create_ap', '--list-running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    return instancias.split('\n')[2].split()[0]

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


#regresa una version mas confiable de mac e Ip
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


def getMacIP(ip, ipMacs):
    for m, i in ipMacs:
        if i == ip:
            return m
    return None

def getNameMac(mac, users):
    for m, n in users:
        if mac == m:
            return n
    return None

def getNameIP(ip, ipMacs, users):
    mac = getMacIP(ip, ipMacs)
    return getNameMac(mac, users)

def getName(ip, macsFile, ap):
    pid = getPid()
    users = getUsers(macsFile)
    ipMacs = getIPMacsConectados(ap)
    name = getNameIP(ip, ipMacs, users)
    if not name:
        name = 'desconocido: %s' % getMacIP(ip, ipMacs)
    return name



class Monitor():
    def __init__(self, macsFile, ap='ap0', port=9031):        
        self.port = port
        self.lock = multiprocessing.Lock()
        self.ap = ap
        self.macsFile = macsFile
        
        
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
            attendThread = WorkThread(conn, addr, self.macsFile, self.ap) # se crea un hilo de atención por cliente
            attendThread.start()

            
class WorkThread(multiprocessing.Process):  # it is actually a subprocess
    def __init__(self, conn, addr, macsFile, ap):
        self.conn = conn
        self.addr = addr
        self.macsFile = macsFile
        self.ap = ap
        multiprocessing.Process.__init__(self)

    def run(self):
        data = ''
        # Se recibe 1  cosas en la serializacion: ip
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
        data = data.strip()
        salida = getName(data, self.macsFile, self.ap)
        # responder algo
        mensaje = str(salida) + '$$$'
        self.conn.sendall(mensaje.encode())
        self.conn.close()


if __name__ == '__main__':

    demonio = Monitor(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    demonio.run()


    
