FROM python
RUN pip install django
RUN mkdir "/code" 
COPY "./notificacionesAP" "/code"
WORKDIR "/code"
ENV PUERTO "8000"
ENV DOMINIO "0.0.0.0"
RUN chmod 755 "runServer.sh" 
CMD /bin/bash -c './runServer.sh "$DOMINIO" "$PUERTO"'