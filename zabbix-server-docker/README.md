# What is [![Zabbix](https://img.shields.io/badge/ZABBIX-FF0000?style=plastic&logo=zotero&logoColor=write)]()?

Zabbix is an open-source monitoring software tool used to monitor and track performance and availability of servers, networks, applications, and services. It provides real-time monitoring, alerting, and visualization of data. Zabbix can be used to monitor various metrics such as CPU usage, memory usage, disk space, network traffic, and more. It is highly scalable and can be customized to meet the specific monitoring needs of an organization.

+ **The Zabbix installation for monitoring network assets can be installed in three ways:** 
    
   * Installation from source code
   * Installation from packages
   * Docker Image

In this tutorial we will cover the installation of Zabbix Server via Docker.

### Install [![Docker](https://img.shields.io/badge/Docker-2496ED?style=plastic&logo=docker&logoColor=white)]() Engine on Ubuntu

**OS requirements🔗**

+ **To install Docker Engine, you need the 64-bit version of one of these Ubuntu versions:**

    * Ubuntu Lunar 23.04
    * Ubuntu Kinetic 22.10
    * Ubuntu Jammy 22.04 (LTS)
    * Ubuntu Focal 20.04 (LTS)
    * Ubuntu Bionic 18.04 (LTS)
 
+ Docker Engine is compatible with `x86_64` (or `amd64`), `armhf`, `arm64`, and `s390x` architectures.

#### Uninstall old versions

Older versions of Docker went by the names of `docker`, `docker.io`, or `docker-engine`, you might also have installations of `containerd` or `runc.` Uninstall any such older versions before attempting to install a new version:

    sudo apt-get remove docker docker-engine docker.io containerd runc

> `apt-get` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren’t automatically removed when you uninstall Docker. If you want to start with a clean installation, and prefer to clean up any existing data, read the uninstall Docker Engine section.

### Install using shell script

If you wish, there is the option to run the automatic Docker installation script `install-docker.sh`. After accessing the **zabbix/zabbix-server-docker** repository, type the following command:

      ./install-docker.sh

Now just wait for the installation to finish!

### Install using the apt repository

Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.

**Set up the repository**

- [ ] **1. Update the `apt` package index and install packages to allow apt to use a repository over HTTPS:**

        sudo apt-get update
        sudo apt-get install ca-certificates curl gnupg
        
- [ ] **2. Add Docker’s official GPG key:**

        sudo install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        sudo chmod a+r /etc/apt/keyrings/docker.gpg

- [ ] **3. Use the following command to set up the repository:**

        echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

### Install Docker Engine

- [ ] **1. Update the apt package index:**

         sudo apt-get update

- [ ] **2. Install Docker Engine, containerd, and Docker Compose.**

         sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

- [ ] **3. Verify that the Docker Engine installation is successful by running the `hello-world` image.**

         sudo docker run hello-world

> This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

---

> Source: https://docs.docker.com/engine/install/ubuntu/

---

### Install Docker-compose

- [ ] **1. Installing docker-compose**

      curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose 
      chmod +x /usr/local/bin/docker-compose                                                                                                  

   - **Check the version of the Docker-Compose**

         docker-compose version 

- [ ] **2. Installing docker-compose using python-pip**

   - **Install python-pip**
   
         sudo apt update
         sudo apt install python3-pip
         
   - When the installation is complete, verify the installation by checking the pip version:
      
         pip3 --version
    
   - **Install docker-compose**

         sudo pip install docker-compose   
------------

## Install Zabbix Server

The Zabbix Server installation will be based on the settings present in the docker-compose.yml file, the file is in this repository.

The first step is to define a location to perform the repository clone. In this tutorial the location `/home` was chosen

    cd /home
    git clone https://github.com/PauloBigooD/Zabbix.git
    cd Zabbix/zabbix-server-docker

If we run the `ls` command we can see the docker-compose.yml file.
    
[![Zabbix](https://uploaddeimagens.com.br/images/004/574/976/full/ls-zabbix-server-docker.png?1691948983)]()

Now it is possible to run the services present in the `docker-composer.yml` file, if you so wish, just run the following command:

      docker compose up -d

[![Zabbix](https://uploaddeimagens.com.br/images/004/575/001/full/docker-compose-up-d.png?1691950921)]()

For security reasons, it might be interesting to change some variables in the docker-compose.yml file. These changes must be made without `docker compose` running, to confirm run the following commands: `docker compose stop` and `docker compose rm -f`. Now adjust the following variables as needed.

```yml
    environment:                                                # Username, password and database name variables
      POSTGRES_USER: zabbix                                     # Database user
      POSTGRES_PASSWORD: zabbix                                 # Database password
      POSTGRES_DB: zabbix                                       # Database name
```

Note that these variables appear more than once in the file and all occurrences must be adjusted.

```yml
    environment:
      GF_SECURITY_ADMIN_PASSWORD: Grafana                        # Grafana admin user access password
```

When completing the necessary adjustments, provision the services again

      docker compose up -d

### How to access Zabbix Server and Grafana API?

To access the Zabbix API, we just need to access a WEB browser and access the following address:

http://127.0.0.1:80

By entering the address above you will be redirected to the following page:

[![Zabbix](https://uploaddeimagens.com.br/images/004/575/013/full/login.png?1691952921)]()

To access, simply enter the following information in the login and password fields:
```
Login: Admin
Password: zabbix
```

After login, you will be redirected to the following screen:

[![Zabbix](https://uploaddeimagens.com.br/images/004/575/014/full/dash.png?1691953034)]()

---

### Note that the Grafana Server service is also provisioned in this deployment. 

To access grafana, go to the following address:

http://127.0.0.1:3000

By entering the address above you will be redirected to the following page:

[![Grafana](https://uploaddeimagens.com.br/images/004/719/611/original/grafana_login.png?1705946573)]()

To access, simply enter the following information in the login and password fields:

```
Login: admin
Password: Grafana
```

After login, you will be redirected to the following screen:

[![Grafana](https://uploaddeimagens.com.br/images/004/719/616/original/welcome_grafana.png?1705946757)]()