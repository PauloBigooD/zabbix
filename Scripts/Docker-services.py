#!/usr/bin/python
# Este script utiliza encoding: utf-8

#####################################################################################################

import subprocess
import json
import re

subprocess.Popen("docker container prune -f", shell=True, stdout=subprocess.PIPE).stdout.readlines()
strings = subprocess.Popen('docker ps -a --format "{{.ID}} {{.Names}} {{.Image}} {{.Status}}" ', shell=True, stdout=subprocess.PIPE).stdout.readlines()

l=list()

for string  in strings:
        string = string.split()
	#print(string)
        
	d=dict()
	
	status = subprocess.Popen('docker inspect --format " {{.State.Status}} " %s' % (string[1]) , shell=True, stdout=subprocess.PIPE).stdout.readlines()					
     	status = status[0].replace('\n','').strip()

	if status == 'running':
	        status=10
	elif status == 'created':
	        status=1
	elif status == 'restarting':
	        status=2
	elif status == 'removing':
	        status=3
        elif status == 'paused':
                status=4
        elif status == 'exited':
                status=5
        elif status == 'dead':
                status=6
    		
	d['{#ZD_STATUS}']=status

	if string[3][0:2] == "Up":
                d['{#ZD_ID}']=string[0]
                d['{#ZD_IMAGE}']=string[2]
                #regex = "^(\w|[-_]|\d)+\."
                #str = string[1]
                #inicio = re.search(regex,str)
                #if inicio:
                #        inicio = inicio.start()
                #fim = re.search(regex,str)
                #if fim:
                #        fim = fim.end() - 1
                d["{#ZD_NAME}"]= string[1] #[inicio:fim]


	l.append(d)

s_json=dict()

s_json["data"]=l

print(json.dumps(s_json,indent=2))