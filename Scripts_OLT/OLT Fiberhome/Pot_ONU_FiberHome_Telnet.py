#!/usr/bin/python
# Este script utiliza encoding: utf-8

import socket
import telnetlib
import shlex
import json

from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

####-Estes campos devem ser alterados de acordo com as especificaçoes de cada cliente

zbx        = '127.0.0.1' # IP do Zabbix para o zabbix-sender
user       = 'GEPON'      # Nome do usuario TELNET
password   = 'GEPON'      # Senha do usuario TELNET
mode       = argv[1]     # check-potencias-onu para coletar a potencia da ONU
olt        = argv[2]     # Nome do host enviado pelo Zabbix
ip         = argv[3]     # IP da OLT enviado pelo Zabbix
community  = argv[4]     # Comunidade do host enviado pelo Zabbix

#- Função para realizar a consulta snmpwalk
def snmpwalk(ipaddr, oid, community):
    result = []
    attempts = 3
    params = ["/usr/bin/snmpbulkwalk", "-v2c", "-r3", "-Ir", "-Oqv", "-c", community, ipaddr, oid] #-Oqv only prints the value, which is good for script
    for attempt in range(attempts):
        snmp = Popen(params, stdout=PIPE, stderr=STDOUT)
        output = snmp.communicate()[0]
        if not snmp.poll():
            break
    for snmpline in output.splitlines():
        result.append(snmpline)
    return result

try:
	tn = telnetlib.Telnet(ip, timeout=3)
except socket.error as e:
	print "{\"STATUS\": \"2\",\"ERROR\": \"" + str(e) + "\"}"
	exit()


# Realiza conexao Telnet
firm_version = tn.read_until("Login: ")
tn.write(user + "\n")
tn.read_until("Password: ")
tn.write(password + "\n")
tn.read_until("User> ")
tn.write("en" + "\n")
tn.read_until("Password: ")
tn.write(password + "\n")
tn.read_until("Admin# ")

tn.write("cd service" + "\n")
tn.read_until("Admin\service# ")
tn.write("terminal length 0" + "\n")
tn.read_until("Admin\service# ")
tn.write("cd .." + "\n")
tn.read_until("Admin# ")

#print("Conexão ok")

if mode == 'check-potencias-onu':
    #- cria um array com todos os mac's das onu's 
    mac_list = snmpwalk(ip, '.1.3.6.1.4.1.5875.800.3.10.1.1.10', community)
    #- a função replace remove as " " que vem na consulta snmpwalk
    length = len(mac_list)

    for i in range(length):
        mac_list[i] = mac_list[i].replace('"', '')

    #- se habilarmos o print veremos que a lista agora vem sem as ""
    #print(mac_list)

    #- cria um json vazio para alocar os valores da coleta 
    response = []

    for mac in mac_list:
        # Entra no menu Telnet adequado 
        tn.write("cd gpononu" + "\n")
        tn.read_until("Admin\gpononu# ")
        tn.write("show whitelist phy_addr select address " + mac + "\n")
        buffer = tn.read_until("Admin\gpononu# ")
        qtdOnu = buffer.split()[-3]

        if "ITEM=0" in qtdOnu:
            print([dict(STATUS="2",ERROR="ONU {} não encontrado".format(mac))])
        else:
            slot    = buffer.split()[-7]
            pon    = buffer.split()[-6]
            onuid  = buffer.split()[-5]
            tn.write("show optic_module slot " + slot + " link " + pon + " onu " + onuid + "\n")
            buffer = tn.read_until("Admin\gpononu# ")
            onu_info = buffer.splitlines()
            onu_info = onu_info[4:-1]

            #- Coleta as informações pertinentes 
            for info in onu_info:
                label = info.split(':')[0].strip()
                value = info.split(':')[1].split('(')[0].strip()
                if label == 'TEMPERATURE':
                    temp = value
                if label == 'VOLTAGE':
                    volt = value
                if label == 'BIAS CURRENT':
                    bias = value
                if label == 'SEND POWER':
                    power = value
                if label == 'RECV POWER':
                    pot = value
            response.append({
                "{#MAC}" : mac, 
                "{#RECV_POWER}" : pot or '',
                "{#TEMPERATURE}" : temp or '',
                "{#VOLTAGE}" : volt or '',
                "{#BIAS_CURRENT}" : bias or '',
                "{#SEND_POWER}" : power or '',
            })

    #- A função json.dumps transforma o dict em um json válido
    data = json.dumps({"data": response})
    print(data)            
    
    #- Encerra a conexão Telnet
    tn.write("cd .." + "\n")
    tn.read_until("Admin# ")
    tn.write("exit" + "\n")
    tn.read_until("User> ")
    tn.write("exit" + "\n")
    exit()