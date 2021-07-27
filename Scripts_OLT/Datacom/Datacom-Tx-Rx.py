#!/usr/bin/python
# Este script utiliza encoding: utf-8

import paramiko
import subprocess
import shlex
import json
import re


from paramiko import SSHClient
from sys import argv
from itertools import groupby
from subprocess import Popen, PIPE, STDOUT

mon     = '127.0.0.1'	# IP do Zabbix-Server
sw      = argv[1]	    # IP do Switch
passSW  = '*****'       # Senha de acesso ao Switch via SSH
userSW  = '*****'		# Usuario de acesso ao Switch via SSH
portSW  = '22'
modo    = argv[2]       # Escolha entre - Rx, Tx, Temp, Volt, Corr
inter   = argv[3]

p = paramiko.SSHClient()
p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
p.connect(sw, port=portSW, username=userSW, password=passSW)
stdin, stdout, stderr = p.exec_command("show interface transceivers ten-gigabit-ethernet 1/1/7")
results = stdout.readlines()

if modo == "Rx":
        print(float(results[17].replace('Rx-Power   [dBm] : ','').split(" [-26.57 ~   -6.0]")[0].strip()))                                                                                                              
elif modo == "Tx":
	print(float(results[16].replace('Tx-Power   [dBm] :   ','').split(" [  -2.0 ~   4.99]")[0].strip()))
elif modo == "Temp":
	print(float(results[13].replace('Temperature  [C] :  ','').split(" [ -10.0 ~   85.0]")[0].strip()))
elif modo == "Volt":
	print(float(results[14].replace('Voltage 3.3V [V] :   ','').split(" [  2.79 ~   3.59]")[0].strip()))
elif modo == "Corr":
	print(float(results[15].replace('Current     [mA] :  ','').split(" [  25.0 ~  110.0]")[0].strip()))
