#### Instruções para subir do Docker-Compose ####

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

