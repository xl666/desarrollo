from django.http import HttpResponse
from monitorAP import settings
import socket

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def keep_alive(request):
    ip = get_client_ip(request)
    mySocket = socket.socket()
    mySocket.connect(('localhost',settings.puertoMonitor))
    message = ip
    mySocket.sendall(message.encode())
    mySocket.sendall('$$$'.encode())        
    mySocket.close()

    contenido = """
    <html>
       <script>
          %s
          setTimeout(function(){
          window.location.reload(1);
           }, 3000);
       </script>
       <body>
          <h1>Keep Alive</h1>
       </body>
    </html>
    """

    return HttpResponse(contenido % (''))
