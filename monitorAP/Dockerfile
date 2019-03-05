FROM alpine
RUN echo "http://dl-3.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add python3 arp-scan
RUN mkdir "/code" 
COPY "./servicioMonitor.py" "/code"
COPY "./runServer.sh" "/code"
WORKDIR "/code"
ENV DOMINIO_SERVICIO_NOMBRES "192.168.12.1"
ENV PUERTO_SERVICIO_NOMBRES "9031"
ENV URL_SERVICIO_NOTIFICACION "http://localhost:8000/guardarMensaje"
ENV INTERFACE "wlo1"
ENV DOMINIO "192.168.12.0/24"
RUN chmod 755 "runServer.sh"
RUN rm -R /var/cache/apk
CMD /bin/sh -c './runServer.sh'