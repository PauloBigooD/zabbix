#!/bin/bash
# Contato: pauloeduardojunior19@gmail.com
# Script utilizado para coleta de informações do quantitativo das ONU's da OLT FiberHome
# $1 - Modo de operação (total, slot, pon)
# $2 - Endereço IP da OLT
# $3 - Porta da comunicação SNMP, geralmete 161
# $4 - Comunidade SNMP
# $5 - Slot da OLT - 1, 2 ,3 ...
# $6 - PON da OLT - 1, 2 ,3 ...

if [ "$1" = "total" ]; then
        snmpbulkwalk -v2c -c $4 $2:$3 1.3.6.1.4.1.5875.800.3.10.1.1.11 | wc -l
fi

if [ "$1" = "slot" ]; then
        snmpbulkwalk -v2c -c $4 $2:$3 1.3.6.1.4.1.5875.800.3.10.1.1.2 | grep ": $5$" | wc -l
fi

if [ "$1" = "pon" ]; then

        #Obtém lista de índices por Slot
        list=$(snmpbulkwalk -v2c -c $4 $2:$3 1.3.6.1.4.1.5875.800.3.10.1.1.2 | grep ": $5$" | cut -d'.' -f9 | cut -d' ' -f1)
        list=$(echo $list | tr ' ' '|')

        #Obtém contagem de ONUs por PON
        snmpbulkwalk -v2c -c $4 $2:$3 1.3.6.1.4.1.5875.800.3.10.1.1.3 | egrep $list | grep ": $6$" | wc -l
fi
