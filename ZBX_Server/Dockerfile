FROM zabbix/zabbix-server-pgsql:ubuntu-latest 
USER root
RUN apt update
RUN ln -fs /usr/share/zoneinfo/America/Recife /etc/localtime
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata 
RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim php-snmp php php-fpm php-opcache python3 python3-pip snmp -y
RUN pip3 install pyTelegramBotAPI
