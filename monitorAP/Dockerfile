FROM alpine
RUN apk add python3
RUN pip3 install django
RUN mkdir "/code" 
COPY "./monitorAP" "/code"
COPY "./servicioMonitor.py" "/code"
COPY "./runServer.sh" "/code"
WORKDIR "/code"
ENV DOMINIO_SERVICIO_NOMBRES "192.168.12.1"
ENV PUERTO_SERVICIO_NOMBRES "9031"
ENV PUERTO "9131"
ENV URL_SERVICIO_NOTIFICACION "http://localhost:8000/guardarMensaje"
ENV DOMINIO_SERVIDOR_WEB "0.0.0.0"
ENV PUERTO_SERVIDOR_WEB "9595"
RUN chmod 755 "runServer.sh"
RUN rm -R /var/cache/apk
CMD /bin/sh -c './runServer.sh "$DOMINIO" "$PUERTO"'