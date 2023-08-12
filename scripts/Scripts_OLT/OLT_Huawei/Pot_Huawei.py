#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

index        = argv[1]     # Index snmp
ip           = argv[3]		# IP do host enviado pelo Zabbix
community    = argv[4]	# Comunidade do host enviado pelo Zabbix
olt          = argv[5]

def snmpwalk(ipaddr, oid, community):
	result   = []
	attempts = 3
	params   = ["/usr/bin/snmpwalk", "-v2c", "-r3", "-Oqv", "-c", community, ipaddr, oid+index]
	for attempt in range(attempts):
		snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result

def PotenciaOpticaOnu(ip, community):
	POTs = snmpwalk(ip,'1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.', community)
	return POTs

def EmailOnu(ip, community):
	EMAILs = snmpwalk(ip,'1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9.', community)
	return EMAILs

potencias = PotenciaOpticaOnu(ip, community)
emails    = EmailOnu(ip, community)
print(float(potencias[0]))