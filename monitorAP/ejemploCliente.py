
import socket
import sys
 
def main(ip, host='localhost', port=9131):
        mySocket = socket.socket()
        mySocket.connect((host,port))
        message = ip
        mySocket.sendall(message.encode())
        mySocket.sendall('$$$'.encode())        
        mySocket.close()
 
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2],int(sys.argv[3]))
