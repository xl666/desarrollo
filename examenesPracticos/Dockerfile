FROM alpine
RUN apk add python3
RUN pip3 install django
RUN mkdir "/code"
RUN mkdir "/service"
COPY "./runServer.sh" "/service"
WORKDIR "/code"
ENV DOMINIO_SERVICIO_NOMBRES "192.168.12.1"
ENV PUERTO_SERVICIO_NOMBRES "9031"
ENV DOMINIO_SERVIDOR_WEB "0.0.0.0"
ENV PUERTO_SERVIDOR_WEB "8100"
ENV DIRECTORIO_RESPUESTA "prueba"
ENV TEMPLATE_EXAMEN "prueba.html"
RUN chmod 755 "/service/runServer.sh"
RUN rm -R /var/cache/apk
CMD /bin/sh -c '/service/runServer.sh'