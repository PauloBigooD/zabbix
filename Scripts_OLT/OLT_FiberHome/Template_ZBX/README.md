

###############-Esta template é compatível com Zabbix 3.4-######################

=> Para que o Zabbix realize o monitoramento da OLT Fiberhome devemos adicionar
   o scrips de coleta em um dos caminhos a baixo, isso vai depender do modo de 
   instalação do Zabbix.

        /etc/zabbix/externalscripts
        
        /usr/lib/zabbix/externalscripts
        
=> Os scripts são os seguintes 
        
        pot_fiberhome.php
        
        name_fiberhome.php
        
        fiberhome.py
        
        total_ONU.py
        
=> Feito isso precisamos dar permissão de excução a todos os scripts, assim como
   permissões de usuario.

        chmode +x "nome do script"
        chown zabbix. "nome do script"
        
=> Por fim devemos alterar as macros na API do Zabbix, essas macros são de suma
   importancia uma vez que não estando devidamente setada a coleta não será
   realizada
   
        {$OLTID} : "Ip da OLT sob monitoramento"
        
        {$SNMP_COMMUNITY} : "Comunidade SNMP da OLT"

        
        