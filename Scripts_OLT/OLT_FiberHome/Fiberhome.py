
#!/usr/bin/python
# Este script utiliza encoding: utf-8
#Contato: pauloeduardodojunior19gmail.com 
# Exemplo de teste: ./fiberhome.py "run" "OLT_FIBERHOME" 192.168.30.3:161 "gpon"


import shlex
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

mon       = '127.0.0.1'	    # IP do Zabbix
mode      = argv[1]	    # launch para disparar e run para executar como subprocesso
olt       = argv[2]         # Nome do host enviado pelo Zabbix
ip        = argv[3]	    # IP do host enviado pelo Zabbix
community = argv[4]	    # Comunidade do host enviado pelo Zabbix

def snmpwalk(ipaddr, oid, community):
	result   = []
	attempts = 3
	params   = ["/usr/bin/snmpbulkwalk", "-v2c", "-r3", "-Oqv", "-c", community, ipaddr, oid] #-Oqv only prints the value, which is good for script
	for attempt in range(attempts):
		snmp   = Popen(params, stdout=PIPE, stderr=STDOUT)
		output = snmp.communicate()[0]
		if not snmp.poll():
			break
	for snmpline in output.splitlines():
		result.append(snmpline)
	return result

def send_zabbix(jstring, olt, key):
 	# Verificar onde é o caminho do zabbix_sender, em caso de dúvida executar linha do comando manualmente
	send = shlex.split("/usr/local/bin/zabbix_sender -z " + mon + " -s \"" + olt + "\" -k " + key + " -o")
	send.append(jstring)
	send = Popen(send, stdout=PIPE, stderr=STDOUT)

def ocupationDiscovery(ip, community):
	# Executa os walks
	slot  = snmpwalk(ip, '.1.3.6.1.4.1.5875.800.3.10.1.1.2', community)
	pon   = snmpwalk(ip, '.1.3.6.1.4.1.5875.800.3.10.1.1.3', community)
	total = str(len(slot))

	# Cria as tuplas Slot/PON
	walk = []
	for i, line in enumerate(slot):
		walk.append([line, pon[i]])

	# Agrupa as listas de Slots e PONs
	slot = []
	pon  = []
	for i, group in groupby(walk, lambda x: x[0]):
		slot.append(list(group))
	for i, line in enumerate(slot):
		for j, group in groupby(line, lambda x: x[1]):
			pon.append(list(group))

	# Envia total de ONUs
	send_zabbix(total, olt, 'total')

	# Envia ocupação dos Slots
	series      = []
	pointValues = []
	series      = "{\"data\":["
	for i, slots in enumerate(slot):
		if i == len(slot)-1:
			pointValues = "{\"{#SLOT}\":\"" + slots[0][0] + "\",\"{#VALOR}\":\"" + str(len(slots)) + "\"}"
		else:
			pointValues = "{\"{#SLOT}\":\"" + slots[1][0] + "\",\"{#VALOR}\":\"" + str(len(slots)) + "\"},"
		series = series + pointValues
	series = series + "]}"
	send_zabbix(series, olt, 'slots')

	# Envia ocupação das PONs
	series      = []
	pointValues = []
	series      = "{\"data\":["
	for i, pons in enumerate(pon):
		if i == len(pon)-1:
			pointValues = "{\"{#SLOT}\":\"" + pons[0][0] + "\",\"{#PON}\":\"" + pons[0][1] + "\",\"{#VALOR}\":\"" + str(len(pons)) + "\"}"
		else:
			pointValues = "{\"{#SLOT}\":\"" + pons[1][0] + "\",\"{#PON}\":\"" + pons[0][1] + "\",\"{#VALOR}\":\"" + str(len(pons)) + "\"},"
		series = series + pointValues
	series = series + "]}"
	send_zabbix(series, olt, 'pons')

if mode == 'launch':
	# ATENÇÃO! - Verificar o caminho do script
	p = shlex.split("/etc/zabbix/externalscripts/fiberhome.py run \"" + olt + "\" " + ip + " " + community)
	p = Popen(p, stdout=PIPE, stderr=STDOUT)
	print ("OK")
	
elif mode == 'run':
	ocupationDiscovery(ip, community)



