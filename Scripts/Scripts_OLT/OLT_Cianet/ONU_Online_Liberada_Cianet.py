#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

ip                     = argv[1]     # Nome do host enviado pelo Zabbix
community              = argv[2]     # Comunidade do host enviado pelo Zabbix
modo                   = argv[3]     # Escolha entre Online ou Liberadas

# Definindo a  função responsável pela comunicação SNMP
def snmpwalk(ipaddr, oid, community):
        result         = []
        attempts       = 3
        params         = ["/usr/bin/snmpbulkwalk", "-v2c", "-r3", "-Oqv", "-c", community, ipaddr, oid]
        for attempt in range(attempts):
                snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
                output = snmp.communicate()[0]
                if not snmp.poll():
                        break
        for snmpline in output.splitlines():
                result.append(snmpline)
        return result

# Realizando a coleta das ONU's Online por meio da OID
def ONUonline(ip, community):
        ONUs          = snmpwalk(ip, '.1.3.6.1.4.1.34592.1.3.3.12.1.1.5.1', community)
        totalONU      = 0
        for i, ONU in enumerate(ONUs):
               if int(ONU) == 3:
                       totalONU += 1
        print(int(totalONU))

# Realizando a coleta das ONU's Liberadas por meio da OID
def ONUliberadas(ip, community):
        ONUs          = snmpwalk(ip, '.1.3.6.1.4.1.34592.1.3.3.12.1.1.5.1', community)
        ONUliberadas  = 0
        ONUliberadas  = str(len(ONUs))
        print(int(ONUliberadas))

if modo == "online":
    ONUonline(ip, community)
elif modo == "liberadas":
    ONUliberadas(ip, community)


