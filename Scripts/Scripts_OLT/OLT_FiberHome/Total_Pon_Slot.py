#!/usr/bin/env python
# Este script utiliza encoding: utf-8

import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT, check_output

ip                 = argv[1]	   # IP do host enviado pelo Zabbix
community          = argv[2]	   # Comunidade do host enviado pelo Zabbix
escolha            = argv[3]       # escolha de opção desejada
slot               = argv[4]       # Slot desejado
pon                = argv[5]       # Pon desejada

def snmpbulkwalk(ipaddr, oid, community):
	result         = []
	attempts       = 3
	if escolha == "pon": 
		params     = ["/usr/bin/snmpbulkwalk", "-v2c", "-Ir", "-c", community, ipaddr, oid]
	else:
		params     = ["/usr/bin/snmpbulkwalk", "-v2c", "-Ir", "-Oqv", "-c", community, ipaddr, oid]
	for attempt in range(attempts):
		try:
			snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
			output = snmp.communicate()[0]
			for snmpline in output.splitlines():
				result.append(snmpline)
			return result
		except Exception as e:
			raise 
		else:
			if not snmp.poll():
				break	

def Slot(ip, community):
	cont  = 0
	slots = snmpbulkwalk(ip,'1.3.6.1.4.1.5875.800.3.10.1.1.2', community)
	for v_slot in slots:
		if v_slot == slot:
			cont += 1
	return cont

def Pon(ip, community):
	listIndexPons  = []
	listIndexSlots = []

	Pons = snmpbulkwalk(ip,'1.3.6.1.4.1.5875.800.3.10.1.1.3', community)
	for v_pon in Pons:
		#$print(v_pon)
		valor   = v_pon.split("INTEGER:")[1].strip()            # o split serve para retirar a informação na posição da OID que queremos, nesse caso queremos o valor de retorno
		if valor == pon:
			idx = v_pon.split(".")[8].split("=")[0].strip()   # aqui o split retira a informação na posiçao 8 da OID, essa posição é definida pelo "."
			listIndexPons.append(idx)


	Slots = snmpbulkwalk(ip,'1.3.6.1.4.1.5875.800.3.10.1.1.2', community)
	for v_slot in Slots:
		valor   = v_slot.split("INTEGER:")[1].strip()           # o split serve para retirar a informação na posição da OID que queremos, nesse caso queremos o valor de retorno
		if valor == slot:
			idx = v_slot.split(".")[8].split("=")[0].strip()  # aqui o split retira a informação na posiçao 8 da OID, essa posição é definida pelo "."
			listIndexSlots.append(idx)

	return intersection(listIndexPons, listIndexSlots)

def Total(ip, community):
	contTotal = 0
	totals    = snmpbulkwalk(ip,'1.3.6.1.4.1.5875.800.3.10.1.1.11', community)
	for v_total in totals:
		if int(v_total) == int(1) or int(v_total) == int(2):
			contTotal += 1
	return contTotal
	#return len(totals)
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return len(lst3)

if escolha == "total":
	print(int(Total(ip, community)))
elif escolha == "pon":
	print(int(Pon(ip,community)))
else:
	print(int(Slot(ip, community)))

