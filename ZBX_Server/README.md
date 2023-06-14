# ![](https://assets.zabbix.com/img/logo/zabbix_logo_313x82.png) ![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Docker_%28container_engine%29_logo.svg/1280px-Docker_%28container_engine%29_logo.svg.png)

### Install Docker Engine on Ubuntu

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

--------

## Lista de comandos Docker 

-> **Listar todos os containers que estão em execução ou não**
    
    docker ps [OPTIONS]

-- Options:

`-a, --all`             -> Show all containers (default shows just running)

`-f, --filter filter`   -> Filter output based on conditions provided

`--format string`       -> Pretty-print containers using a Go template

`-n, --last int`        -> Show n last created containers (includes all states) (default -1)

`-l, --latest`          -> Show the latest created container (includes all states)

`--no-trunc`            -> Don't truncate output

`-q, --quiet`           -> Only display container IDs

`-s, --size`            -> Display total file sizes

----

-> **Iniciar um ou mais containers que estejam parados**

    docker start [OPTIONS] CONTAINER [CONTAINER...]

-- Options:

`-a, --attach`           -> Attach STDOUT/STDERR and forward signals

`--detach-keys string`   -> Override the key sequence for detaching a container

`-i, --interactive`      -> Attach container's STDIN

----

-> **Pausar um ou mais conteiners que estejam em execução**

    docker stop [OPTIONS] CONTAINER [CONTAINER...]

-- Options:

`-t, --time int`   -> Seconds to wait for stop before killing it (default 10)

----

-> **Reiniciar um ou mais conteiners**

    docker restart [OPTIONS] CONTAINER [CONTAINER...]

-- Options:

`-t, --time int`   -> Seconds to wait for stop before killing it (default 10)

----

-> **Remover um ou mais conteiners**

    docker rm [OPTIONS] CONTAINER [CONTAINER...]

-- Options:

`-f, --force`     -> Force the removal of a running container (uses SIGKILL)

`-l, --link`      -> Remove the specified link

`-v, --volumes`   -> Remove anonymous volumes associated with the container

----

-> **Listar images dos containers**

    docker images [OPTIONS] [REPOSITORY[:TAG]]

-- Options:

`-a, --all`             -> Show all images (default hides intermediate images)

`--digests`             -> Show digests

`-f, --filter filter`   -> Filter output based on conditions provided

`--format string `      -> Pretty-print images using a Go template

`--no-trunc`            -> Don't truncate output

`-q, --quiet`           -> Only show image IDs

---- 

-> **Remover uma ou mais images**

    docker rmi [OPTIONS] IMAGE [IMAGE...]

-- Options:

`-f, --force`     -> Force the removal a image

`--no-prune`      -> Do not delete untagged parents


----

-> **Verificar uso do container**
    
    docker stats [OPTIONS] [CONTAINER...]

-- Options:

`-a, --all`         -> Show all containers (default shows just running)
      
`--format string`   -> Pretty-print images using a Go template

`--no-stream`       -> Disable streaming stats and only pull the first result

`--no-trunc`        -> Do not truncate output

----

-> **Verificar logs do container**
    
    docker logs [OPTIONS] CONTAINER

-- Options:

`--details`              -> Show extra details provided to logs
      
`-f, --follow`           -> Follow log output

`--since string`     -> Show logs since timestamp (e.g. "2013-01-02T13:23:37Z") or
                       relative (e.g. "42m" for 42 minutes)

`-n, --tail string`      -> Number of lines to show from the end of the logs (default "all")

`-t, --timestamps`       -> Show timestamps

`--until string`     -> Show logs before a timestamp (e.g. "2013-01-02T13:23:37Z") or
                       relative (e.g. "42m" for 42 minutes

----

-> **Gerenciamento dos volumes no Docker**

    docker volume COMMAND

-- Commands:

`create`     -> Create a volume

`inspect`    -> Display detailed information on one or more volumes

`ls`         -> List volumes

`prune`      -> Remove all unused local volumes

`rm`         -> Remove one or more volumes

----

-> **Executa uma instrução dentro do container que está rodando sem precisar atachar nele**

      docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
      
-- Aliases:
      
      docker container exec, docker exec
      
-- Commands:

  `-d, --detach`     -> Detached mode: run command in the background
  
  `--detach-keys string`     -> Override the key sequence for detaching a container
  
  `-e, --env list`     -> Set environment variables
  
   `--env-file list`     -> Read in a file of environment variables
      
  `-i, --interactive`     -> Keep STDIN open even if not attached
  
  `--privileged`    -> Give extended privileges to the command
      
  `-t, --tty`     -> Allocate a pseudo-TTY
  
  `-u, --user string`     -> Username or UID (format: "<name|uid>[:<group|gid>]")
  
  `-w, --workdir string`     -> Working directory inside the container
  
----

-> **Exibe o json com todas as configurações do container**

      docker inspect [OPTIONS] NAME|ID [NAME|ID...]
      
-- Commands:

  `-f, --format string`     -> Format output using a custom template:
                        'json':             Print in JSON format
                        'TEMPLATE':         Print output using the given
                        Go template. Refer to https://docs.docker.com/go/formatting/
                        for more information about formatting output with
                        templates
                        
  `-s, --size`     -> Display total file sizes if the type is container
  
  `--type string`     -> Return JSON for specified type
      
----

-> **Clusterização das aplicações em uma orquestração de várias containers**

       docker swarm COMMAND

-- Commands:

  `ca`     -> Display and rotate the root CA
  
  `init`     -> Initialize a swarm
  
  `join`     -> Join a swarm as a node and/or manager
  
  `join-token`     -> Manage join tokens
  
  `leave`     -> Leave the swarm
  
  `unlock`     -> Unlock swarm
  
  `unlock-key`     -> Manage the unlock key
  
  `update`     -> Update the swarm

----

> Fonte : [![Docker](https://img.shields.io/badge/Docker-2496ED?style=plastic&logo=docker&logoColor=white)](https://docs.docker.com/engine/reference/commandline/docker/)
