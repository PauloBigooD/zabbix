# Overview
Zabbix agent is deployed on a monitoring target to actively monitor local resources and applications (hard drives, memory, processor statistics, etc.).

The agent gathers operational information locally and reports data to Zabbix server for further processing. In case of failures (such as a hard disk running full or a crashed service process), Zabbix server can actively alert the administrators of the particular machine that reported the failure.

Zabbix agents are extremely efficient because of use of native system calls for gathering statistical information.

## Passive and active checks
Zabbix agents can perform passive and active checks.

 - In a passive check the agent responds to a data request. Zabbix server (or proxy) asks for data, for example, CPU load, and Zabbix agent sends back the result.

 - Active checks require more complex processing. The agent must first retrieve a list of items from Zabbix server for independent processing. Then it will periodically send new values to the server.

 - Whether to perform passive or active checks is configured by selecting the respective monitoring item type. Zabbix agent processes items of type 'Zabbix agent' or 'Zabbix agent (active)'.

### Official manual

>See the [package installation](https://www.zabbix.com/documentation/current/en/manual/installation/install_from_packages) section for instructions on how to install Zabbix agent as package.

>Alternatively see instructions for [manual installation](https://www.zabbix.com/documentation/current/en/manual/installation/install#installing-zabbix-daemons) if you do not want to use packages.

---

Check the following variables from the zabbix_agent2.conf file

```ỳml
  Server=IP-Zabbix-Server

  ServerActive=IP-Zabbix-Server:10051

  Hostname=Host-Name
```
