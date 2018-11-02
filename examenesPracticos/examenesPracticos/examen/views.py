
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from examen import settings
import shutil
from django.shortcuts import redirect
import socket

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def pedirNombre(ip):
        mySocket = socket.socket()
        mySocket.connect((settings.servicioNombreHost, int(settings.servicioNombrePort)))
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

def subir(request):
    if request.method == 'GET':
        t = loader.get_template(settings.examenTemplate)
        request_context = RequestContext(request, {})
        return HttpResponse(t.template.render(request_context))
        
        
    elif request.method == 'POST' and request.FILES['archivo']:
        ar = request.FILES['archivo']
        ip = get_client_ip(request)
        alumno = pedirNombre(ip)

        path = ar.name
        directorio = settings.BASE_DIR + ('/%s/' % settings.RES_DIR) + alumno
           
        try:
            if os.path.exists(directorio):
                shutil.rmtree(directorio)
            else:
                os.mkdir(directorio)
            fs = FileSystemStorage()
            fs.save(directorio+'/'+path, ar)
        except Exception as err:
            print('Erorororororo')
            print(err)
            return redirect('/fallo')        

        return redirect('/final')


def final(request):
    return render_to_response('final.html')

def fallo(request):
    return render_to_response('error.html')
    
def bajar(request):
    return redirect('/static/programacion.zip')
