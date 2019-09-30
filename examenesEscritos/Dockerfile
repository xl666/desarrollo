# start from an official image
FROM python:3.6.7

RUN apt-get -y update
RUN mkdir -p /code
RUN mkdir "/system"
COPY requirements.txt "/system"
RUN pip install -r /system/requirements.txt


WORKDIR /code


EXPOSE 8000

ENV SECRET_KEY_DEVELOPMENT=""
ENV SECRET_KEY_PRODUCTION=""
ENV DATABASE_NAME=""
ENV DATABASE_USER=""
ENV DATABASE_PASSWORD=""
ENV DATABASE_HOST=""
ENV DATABASE_PORT=3306
ENV URL_SERVICIO_NOTIFICACION="http://localhost:8000/guardarMensaje"

COPY iniciarServidor.sh "/system"
RUN chmod 755 "/system/iniciarServidor.sh"


CMD /bin/bash -c '/system/iniciarServidor.sh'
