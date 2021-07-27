**Primeiramente acessar a pasta raiz de instalação do zabbix :**

        cd /etc/zabbix/externalscripts

**Fazer o download do script que realiza a descoberta dos discos :** 

        wget https://raw.github.com/dkanbier/zabbix-linux/master/LLD/queryDisks.pl

**Agora precisamos adicionar permissão de execução o script com o comando :** 

        chmod +x queryDisks.pl

**O próximo passo é dar permissão de execução ao script :**

        chown -R zabbix: queryDisks.pl
        
**Para testarmos o script utilizamos :**

        ./queryDisks.pl

**O retorno do teste do script é algo parecido com isso :**

        {
         "data":[
          { "{#DISK}":"ram0" },
          { "{#DISK}":"ram1" },
          { "{#DISK}":"sda" },
          { "{#DISK}":"sda1" }
         ]
        }

**Agora precisamos acessar a conf. do agent :**

        nano /etc/zabbix/zabbix_agentd.conf

**E adicionar o seguinte userparameter :**

        UserParameter = custom.vfs.dev.discovery[*],/etc/zabbix/externalscripts/queryDisks.pl

**Agora precisamos reiniciar o agent zabbix :**

        service zabbix-agent restart

**Feito isso devemos colocar esse arquivo no diretório “Incluir” do agente Zabbix nos hosts que deseja monitorar, ele permitirá o monitoramento dessas informações usando chaves personalizadas.**

        wget https://raw.github.com/dkanbier/zabbix-linux/master/UserParameters/userparameter_linux_disks.conf
        
        mv userparameter_linux_disks.conf /etc/zabbix/zabbix_agentd.d
        
        service zabbix-agent restart

**Agora para que o Zabbix-server colete tudo direitinho precisamos ir interface WEB, em Administration / General / Regular expressions , na aba das expressões regulares devemos adicionar a seguinte expressão:**

        Name : Disk devices for discovery
        Expressions :  Result is TRUE  ^(sda.*|sdb.*|loop.*|md.*|nvme.*|vd.*|sr.*|s.*|zd.*)$

A expression pode variar de acordo com o HD/Raiz do arquivo, que está sendo monitorado, para isso devemos verificar a resposta do script no passo 5.
Tudo pronto, agora só precisamos aguardar o zabbix começar a coletar as informações.
