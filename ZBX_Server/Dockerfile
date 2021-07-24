FROM zabbix/zabbix-server-pgsql:alpine-4.2.5 

RUN apk update && apk add php7-snmp && apk add php7 php7-fpm php7-opcache\
    python3 --upgrade py-pip net-snmp-tools && pip install pyTelegramBotAPI
