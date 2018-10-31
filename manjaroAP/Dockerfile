
FROM jonathonf/manjaro
RUN pacman -Syy \  
    && pacman -S --noconfirm grep which create_ap gawk glibc wireless_tools net-tools \
    && rm -rf /var/cache/pacman/pkg/*
ENV IWIRELESS wlo1 # interfaz donde estará el AP
ENV IINTERNET wlo1 
ENV ESSID manjaroAP
ENV PASS 12345678
ENV RESTRICTEDMODE ""
ENV RESTRICTMAC ""
ENV ALUMNSMACS ""
ENV WHITEURLS ""
ENV CHANNEL "1"
ENV FORCECHANNEL ""
ENV DIRE "/home"
ENV IPSERVICEPORT "9031"
COPY ./runAP.sh $DIRE
COPY ./obtenerIPs.py $DIRE 
COPY ./servicioIPAlumno.py $DIRE
COPY ./runServicioIP.sh $DIRE
COPY ./monitorizarConexiones.py $DIRE
COPY ./runMonitor.sh $DIRE
RUN chmod 755 $DIRE/runAP.sh \
    && chmod 755 $DIRE/runMonitor.sh
WORKDIR $DIRE
CMD /bin/bash -c '$DIRE/runAP.sh'