#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT
import math

index          = argv[1]            # Index snmp
ip             = argv[2]            # IP do host enviado pelo Zabbix
community      = argv[3]	    # Comunidade do host enviado pelo Zabbix

# Definindo a  função responsável pela comunicação SNMP
def snmpwalk(ipaddr, oid, community):
	result     = []
	attempts   = 3
	params     = ["/usr/bin/snmpbulkwalk", "-v2c", "-r3", "-Oqv", "-c", community, ipaddr, oid+index]
	for attempt in range(attempts):
		snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result

# Realizando a coleta do potência da ONU por meio da OID
def PotenciaOpticaOnu(ip, community):
	POT       = snmpwalk(ip,'1.3.6.1.4.1.34592.1.3.4.1.1.36.', community)
	POT       = float(POT[0])
	POTs      = (10*math.log10(POT)-40)
	return POTs

potencias = PotenciaOpticaOnu(ip, community)
print(potencias)
