# ![](https://assets.zabbix.com/img/logo/zabbix_logo_313x82.png) ![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Docker_%28container_engine%29_logo.svg/1280px-Docker_%28container_engine%29_logo.svg.png)

#### Instruções para subir o Docker-Compose - Sistemas Debian ####

####--Primeiramente precisamos instalar algumas dependências--####

    apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common bash-completion
    
####--Para instalar as dependências utilizamos o seguinte comando--####

     apt-get update                                                                                                
     apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common bash-completion -y 
     
####--Agora é preciso adicionar a public key especifica para o Docker--####

     curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -    
    
####--O próximo passo agora é adicionar o repositório Docker--####

     add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable" 
    
####--Feito isso, agora podemos finalmente instalar o Docker-ce com o seguinte comando--####

     apt install docker-ce 
    

####--Neste momento o Docker já se encontra devidadente instalado, com isso podemos verificar a versão do Docker instalado--####

     docker version 

####--Para setar o restart automático do Docker.service executamos o seguinte comando--####

     systemctl enable docker 
   
####--Instalando o Docker-Compose--###

     curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose 
     chmod +x /usr/local/bin/docker-compose                                                                                                  

####--Para checar a versão do Docker-Compose usamos o seguinte comando--####

     docker-compose version 


############################# Lista de comandos Docker ##############################

-> Listar todos os containers em execusão 
    docker ps
    
-> Listar todos os containers que estão em execução ou não
    
    docker ps -a
    
-> Start, Stop, Restart, Remove
    
    docker start   "Id-Container"
    docker stop    "Id-Container"
    docker restart "Id-Container"
    docker rm      "Id-Container"
    
    docker rm   -f "Id-Container" <--> OBS: Se o container estiver em execusão pode ser preciso forçar a remoção
    
-> Listar imagens dos containers

    docker images
    
-> Verificar uso do container
    
    docker stats


Fonte : https://docs.docker.com/engine/reference/commandline/docker/
