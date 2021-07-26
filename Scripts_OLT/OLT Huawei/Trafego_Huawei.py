#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT


ip        = argv[1]		# IP do host enviado pelo Zabbix
community = argv[2]    	# Comunidade do host enviado pelo Zabbix
index     = argv[3]     # Index snmp
escolha   = argv[4]     # Escolha in para tráfego de entrada 


def snmpwalk(ipaddr, oid, community):
	result   = []
	attempts = 3
	params   = ["/usr/bin/snmpwalk", "-v2c", "-Ir", "-Oqv", "-c", community, ipaddr, oid+index]
	for attempt in range(attempts):
		snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result


def ifHCInOctets(ip, community):
	Ins = snmpwalk(ip,'1.3.6.1.2.1.31.1.1.1.6.', community)
	return Ins

def ifHCOutOctets(ip, community):
	Outs = snmpwalk(ip,'1.3.6.1.2.1.31.1.1.1.10.', community)
	return Outs

if(escolha == "in"):
	print(ifHCInOctets(ip, community))
else:
	print(ifHCOutOctets(ip, community))

