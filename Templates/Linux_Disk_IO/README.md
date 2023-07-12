**1. Acessar a pasta dos externalscripts do zabbix agent:**

        cd /etc/zabbix/externalscripts

**2. Fazer o download do script que realiza a descoberta dos discos:** 

        wget https://raw.github.com/dkanbier/zabbix-linux/master/LLD/queryDisks.pl

**3. Agora precisamos adicionar permissão de execução o script com o comando:** 

        chmod +x queryDisks.pl

**4. O próximo passo é dar permissão de execução ao script:**

        chown -R zabbix: queryDisks.pl
        
**5. Para testarmos o script utilizamos :**

        ./queryDisks.pl

**O retorno do teste do script é algo parecido com isso:**

        {
         "data":[
          { "{#DISK}":"ram0" },
          { "{#DISK}":"ram1" },
          { "{#DISK}":"sda" },
          { "{#DISK}":"sda1" }
         ]
        }

**6. Agora precisamos acessar a conf. do agente:**

        vi /etc/zabbix/zabbix_agentd.conf

> Para agente 2

        vi /etc/zabbix/zabbix_agent2.conf

**7. Adicionar os seguintes userparameter's:**

        UserParameter=custom.vfs.dev.discovery[*],/etc/zabbix/externalscripts/queryDisks.pl
        #
        # reads completed successfully
        UserParameter=custom.vfs.dev.read.ops[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$4}'
        # sectors read
        UserParameter=custom.vfs.dev.read.sectors[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$6}'
        # time spent reading (ms)
        UserParameter=custom.vfs.dev.read.ms[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$7}'
        # writes completed
        UserParameter=custom.vfs.dev.write.ops[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$8}'
        # sectors written
        UserParameter=custom.vfs.dev.write.sectors[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$10}'
        # time spent writing (ms)
        UserParameter=custom.vfs.dev.write.ms[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$11}'
        # I/Os currently in progress
        UserParameter=custom.vfs.dev.io.active[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$12}'
        # time spent doing I/Os (ms)
        UserParameter=custom.vfs.dev.io.ms[*],cat /proc/diskstats | egrep $1 | head -1 | awk '{print $$13}'

**8. Agora precisamos reiniciar o agent zabbix:**

        service zabbix-agent restart

**Agora para que o Zabbix-server colete tudo direitinho precisamos ir interface WEB, em Administration / General / Regular expressions , na aba das expressões regulares devemos adicionar a seguinte expressão:**

        Name : Disk devices for discovery
        Expressions :  Result is TRUE  ^(sda.*|sdb.*|loop.*|md.*|nvme.*|vd.*|sr.*|s.*|zd.*)$

> A expression pode variar de acordo com o HD/Raiz do arquivo, que está sendo monitorado, para isso devemos verificar a resposta do script no passo 5.

**Tudo pronto, agora só precisamos aguardar o zabbix começar a coletar as informações.**
