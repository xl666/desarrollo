from django.http import HttpResponse
from notificacionesAP import settings

def bitacora(request):
    pop = """
    num = Math.random() * 800;
    window.open("/ultimoMensaje/", "AVISO"+ num,"resizable=no,toolbar=no,scrollbars=no,menubar=no,status=no,directories=n o,width="+500+",height="+500+",left="+num+",top="+100+"");
    """
    if not settings.ultimo:
        pop = ''
    
    contenido = """
    <html>
       <script>
          %s
          setTimeout(function(){
           window.location.reload(1);
           }, 5000);
       </script>
       <body>
          <h1>Bitácora</h1>
          <ul>
             %s
          </ul>
       </body>
    </html>
    """
    plantilla = '<li>%s</li>'
    elementos = ''
    if settings.buzon:
        for ele in settings.buzon:
            elementos += plantilla % ele
    
        return HttpResponse(contenido % (pop, elementos))
    return HttpResponse(contenido % ('', 'sin elementos'))


def ultimoMensaje(request):
    if settings.ultimo:
        aux = settings.ultimo
        settings.ultimo = ''
        contenido ='''
        <html>
           <body style="background-color:black;color:white;">
              %s
           </body>
        </html>
        '''
        return HttpResponse(contenido % aux)
    return HttpResponse('')

def guardarMensaje(request):
    
    if request.method == 'GET':
        if not settings.buzon:
            settings.buzon = []
        mensaje = request.GET.get('mensaje')
        if mensaje:
            settings.buzon.append(mensaje)
            settings.ultimo += mensaje
    return HttpResponse('')
