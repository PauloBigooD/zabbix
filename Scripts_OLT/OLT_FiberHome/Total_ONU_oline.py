#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

mon            = '127.0.0.1'	# IP do Zabbix
olt            = argv[1]		# Nome do host enviado pelo Zabbix
ip             = argv[2]		# IP do host enviado pelo Zabbix
community      = argv[3]	    # Comunidade do host enviado pelo Zabbix

def snmpbulkwalk(ipaddr, oid, community):
	result     = []
	attempts   = 3
	params     = ["/usr/bin/snmpbulkwalk", "-v2c", ”-Ir”, "-r3", "-Oqv", "-c", community, ipaddr, oid]
	for attempt in range(attempts):
		snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result

def send_zabbix(jstring, olt, key):
	send = shlex.split("/usr/local/bin/zabbix_sender -z " + mon + " -s \"" + olt + "\" -k " + key + " -o")
	send.append(jstring)
	send = Popen(send, stdout=PIPE, stderr=STDOUT)
	print(jstring)

def ONUonlineDiscovery(ip, community):
	# Executa os walks
	ONUs   = snmpbulkwalk(ip, '.1.3.6.1.4.1.5875.800.3.10.1.1.11', community)
	totalONU = 0
	for i, ONU in enumerate(ONUs):
		if int(ONU) == 1:
			totalONU += 1 
	# Envia total de ONUs online
	#send_zabbix(str(totalONU), olt, 'total')
	print(totalONU)
ONUonlineDiscovery(ip, community)