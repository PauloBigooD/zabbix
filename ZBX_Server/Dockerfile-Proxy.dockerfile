# Dockerfile para Zabbix Proxy baseado em MySQL com sistema operacional Alpine
FROM zabbix/zabbix-proxy-mysql:alpine-4.2.5

LABEL maintainers="Dependencias do Alpine para o Zabbix"

RUN echo 151.101.92.249 dl-cdn.alpinelinux.org >> /etc/hosts && apk update \
        && apk --no-cache add net-snmp net-snmp-tools \
        && echo http://dl-cdn.alpinelinux.org/alpine/v3.4/main >> /etc/apk/repositories \
        && echo http://dl-cdn.alpinelinux.org/alpine/v3.4/community >> /etc/apk/repositories \
        && apk update && apk add php7-snmp && apk add php7 php7-fpm php7-opcache \
        python3 --upgrade py-pip net-snmp-tools && pip install pyTelegramBotAPI

        