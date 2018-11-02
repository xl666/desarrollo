FROM python
RUN pip install django
RUN mkdir "/code" 
COPY "./examenesPracticos" "/code"
COPY "./runServer.sh" "/code"
WORKDIR "/code"
ENV DOMINIO_SERVICIO_NOMBRES "192.168.12.1"
ENV PUERTO_SERVICIO_NOMBRES "9031"
ENV DOMINIO_SERVIDOR_WEB "0.0.0.0"
ENV PUERTO_SERVIDOR_WEB "8100"
ENV DIRECTORIO_RESPUESTA "prueba"
ENV TEMPLATE_EXAMEN "prueba.html"
RUN chmod 755 "runServer.sh" 
CMD /bin/bash -c './runServer.sh'