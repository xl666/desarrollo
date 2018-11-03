FROM alpine
RUN apk add python3
RUN pip3 install django
RUN mkdir "/code" 
COPY "./notificacionesAP" "/code"
WORKDIR "/code"
ENV PUERTO "8000"
ENV DOMINIO "0.0.0.0"
RUN chmod 755 "runServer.sh"
RUN rm -R /var/cache/apk
CMD /bin/sh -c './runServer.sh "$DOMINIO" "$PUERTO"'