#!/usr/bin/env python
# Este script utiliza encoding: utf-8
#Contato: pauloeduardodojunior19gmail.com 

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT
import math

index     = argv[1]            # Index snmp
ip        = argv[2]            # IP do host enviado pelo Zabbix
community = argv[3]        	   # Comunidade do host enviado pelo Zabbix

def snmpwalk(ipaddr, oid, community):
	result   = []
	attempts = 3
	params   = ["/usr/bin/snmpbulkwalk", "-v2c", "-r3", "-Oqv", "-c", community, ipaddr, oid+index]
	for attempt in range(attempts):
		snmp = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result

def PotenciaOpticaOnu(ip, community):
	POT = snmpwalk(ip,'1.3.6.1.4.1.5875.800.3.9.3.3.1.6.', community)
	POTS=int(POT[0])
	return POTS

potencias =(ip, community)
print(potencias)


