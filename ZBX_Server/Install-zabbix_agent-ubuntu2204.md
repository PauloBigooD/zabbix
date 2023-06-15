  # **Install Zabbix repository**
  
    wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-4+ubuntu22.04_all.deb

    dpkg -i zabbix-release_6.0-4+ubuntu22.04_all.deb

    apt update
    
# **Install Zabbix agent**

    apt install zabbix-agent
    
# **Edit zabbix-agent.config**

    vi /etc/zabbix/zabbix_agentd.conf
    
  - Change the following options
      
      `Server=172.31.0.135`
      
      `ServerActive=172.31.0.135`
      
      `Hostname=Informar nome do host`
