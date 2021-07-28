# Dockerfile para Zabbix Server baseado em pgSQL com sistema operacional Ubuntu 4.4
FROM zabbix/zabbix-server-pgsql:ubuntu-4.4-latest 

RUN apt update
RUN ln -fs /usr/share/zoneinfo/America/Recife /etc/localtime
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata 
RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install php-snmp -y
RUN apt-get install php -y
RUN apt-get install php-fpm -y
RUN apt-get install php-opcache -y
RUN apt-get install python3 python3-pip snmp -y
RUN pip3 install pyTelegramBotAPI
RUN rm /var/lib/snmp/mibs/ietf/SNMPv2-PDU