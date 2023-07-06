#!/bin/bash
# 
# Script para execução de backups do servidor Zabbix
# Autor: Werneck Costa - werneck.costa@gmail.com
# Data inicial: 01/04/2015
# Versão 0.0 - Backup de banco
# Versão 0.5 - Adição de arquivos de configuração
# Versão 1.0 - Adição de arquivos web
# Versão 1.5 - Backup de banco, arquivos de configuração e arquivos web, com envio de detalhes por e-mail e arquivos de log
# Segurança contra auto-burrices
#cp $0 ~/$0-"`date +'%d%m%Y-%H%M%S'`"


####################################################################
## Modificado por: Paulo Eduardo - pauloeduardojunior19@gmail.com ##
####################################################################
# Data : 07/10/2019
# 1º- Adaptação para realizar o backup de banco de dados PostgreSQL ao inves de MYSQL.
# 2º- Adaptação para rodar em ambiente Docker.
# 3º- Adição de comentários 
# Versão 2.0 - PostgreSQL, ambiente Zabbix em conteiners.


# Caso queira visualizar os diálogos de conclusão dos passos não comente a variável $ECHO_TELA. Quando configurar o script na rotina automática do "cron" mudar o valor para 0.
ECHO_TELA="1"
# Adicionar o nome da empresa que deseja-mos realizar a rotina de backup.
EMPRESA="Nome da empresa"
SOFTWARE="zabbix"

TEMPO_START="`date +'%s'`"
TEMPO_END="0"
TEMPO_TOTAL="0"

LOG="/home/logicasistemas/backups/scripts/resultado_backup_$SOFTWARE_full.log"
DIR_BACKUP="/home/logicasistemas/backups/$SOFTWARE"
DIR_TEMP="/home/logicasistemas/backups/tmp/tmp-$SOFTWARE"

DIAS_MANTER="5"

########################
## Funções auxiliares ##
########################

######################################################################################################################################
## Função que retorna a data/hora no formato "DD/MM/AAAA - HH:MM:SS" utilizada para logs e "DDMMAAAA-HHMMSS" para nomes de arquivos ##
######################################################################################################################################
datar(){
case $1 in
	log)
		echo `date +'%d/%m/%Y - %H:%M:%S'`
	;;
	file)
		echo `date +'%d%m%Y-%H%M%S'`
	;;
	*)
		echo "Formato não reconhecido"
		exit 1
	;;
	esac
}

#################################################
## Função que registra os logs no arquivo $LOG ##
#################################################
logar(){
if [ $ECHO_TELA == "1" ]
then
	echo -e "$(datar log) -> $*"
fi

if [ -e $LOG ]
then
	echo -e "$(datar log) -> $*" >> $LOG
else
	echo -e "$(datar log) -> $*" > $LOG
fi
}

###############
## Principal ##
###############
logar "---------------------------------------"
logar "$EMPRESA - Backup do sistema $SOFTWARE"
logar "Processo iniciado em $(datar log)"
logar "Criando o diretório temporário $DIR_TEMP"

# Adicionar verificação dos diretórios de Backup (se existem)
if [ ! -e $DIR_BACKUP ]
then
	logar "Diretório $DIR_BACKUP não existe. Será preciso cria-lo manualmente"
	exit 1
fi

###############################################
## Verifica, cria/deleta diretório $DIR_TEMP ##
###############################################
if [ -e "$DIR_TEMP" ]
then
	rm -rf $DIR_TEMP
	mkdir -p $DIR_TEMP
	logar "Diretório existia. Deletado e recriado"
else
	mkdir -p $DIR_TEMP
	logar "Diretório criado"
fi

################################################################################
## Função que verifica se existem arquivos mais antigos que $DIAS_MANTER dias ##
################################################################################
verificar_antigos(){
logar "Verificando a existência de arquivos com tempo maior que $DIAS_MANTER dias"

ARQUIVOS="$(find $DIR_BACKUP -name "*.tar.gz" -mtime +$DIAS_MANTER)"

if [ "x$ARQUIVOS" != "x" ]
then
	logar "Existem arquivos com mais de $DIAS_MANTER dias"
	logar "Excluindo os seguinte arquivos: \n$ARQUIVOS"
	rm -f `find $DIR_BACKUP -name "*.tar.gz" -mtime +$DIAS_MANTER`
	else
		logar "Não será necessária a exclusão de arquivos anteriores."
fi
}

###################################################
## Função que realiza o "dump" no Banco de Dados ##
###################################################
dump_postgresql(){

POSTGRESQL_USER="zabbix"                # Usuario de acesso ao PostgreSQL, deve ser o mesmo configurado no arquivo .YML
POSTGRESQL_PASS="l0g1c251573m25"               # Senha de acesso ao PostgreSQL, deve ser o mesmo configurado no arquivo .YML
POSTGRESQL_DB="zabbix"                 # Nome do banco PostgreSQL, deve ser o mesmo configurado no arquivo .YML

logar "Efetuando o dump do PosrgreSQL" 

docker exec -it -e PGPASSWORD=$POSTGRESQL_PASS <postgres_container_name> pg_dump -U $POSTGRESQL_USER $POSTGRESQL_DB > $DIR_TEMP/$SOFTWARE.sql 

code=$?
if [ $code -eq 0 ]; 
then
	logar "Não foram encontrados erros ao realizar o pg_dump, finalizado com sucesso"
else
	logar "Erros foram encontrados ao realizar o pg_dump"
	exit 1
fi



}

#############################################################
## Função responsável por copiar arquivos da aplicação/web ##
#############################################################
cp_arquivos(){
logar "Juntando os arquivos da aplicação e parte web:"

cp -RP /home/logicasistemas/docker-compose.yml $DIR_TEMP/docker
cp -RP /home/logicasistemas/Dockerfile $DIR_TEMP/docker

docker cp -a "Nome oi ID do container":/etc/zabbix/ $DIR_TEMP/zabbix-app                                        # Copiando configurações do zabbix-server. 
docker cp -a "Nome oi ID do container":/usr/lib/zabbix/alertscripts/ $DIR_TEMP/zabbix-alertscripts              # Copiando os scripts de alerta.
docker cp -a "Nome oi ID do container":/usr/lib/zabbix/externalscripts/ $DIR_TEMP/zabbix-externalscripts        # Copiando os scripts de coleta.
docker cp -a "Nome oi ID do container":/usr/share/zabbix/ $DIR_TEMP/zabbix-web                                  # Copiando configurações do zabbix-web.

logar "Cópia do arquivo da aplicação efetuada"
}

##############################################################
### Função responsável por compactar os arquivos do Backup ###
##############################################################
targz_todos(){
logar "Aplicando tar + gzip nos arquivos em $DIR_TEMP (arquivos: $(ls -m $DIR_TEMP ))"

ERR_TAR="$DIR_TEMP/erro-tar.txt"
RES_TAR="$(tar czf $DIR_BACKUP/$SOFTWARE.tar.gz $DIR_TEMP/* 2>$ERR_TAR;echo $?)"

if [ "$RES_TAR" != "2" ]
then
	logar "Tar Ok"
else
	logar "Problemas com o Tar: $(cat $ERR_TAR)"
	exit 1
fi

ARQUIVO="$SOFTWARE-$(datar file)"

logar "Alterando o nome do arquivo para permanência temporária de $DIAS_MANTER dias ($SOFTWARE.tar.gz -> $ARQUIVO.tar.gz)"
mv $DIR_BACKUP/$SOFTWARE.tar.gz $DIR_BACKUP/$ARQUIVO.tar.gz
}

########################################
## Função de limpeza de dados antigos ##
########################################
finalizacao(){
logar "Limpando os dados salvos em $DIR_TEMP"
rm -rf $DIR_TEMP

logar "Backup finalizado"

TEMPO_END="`date +'%s'`"
TEMPO_TOTAL=$(( TEMPO_END - TEMPO_START ))

logar " "
logar "Tempo total: $TEMPO_TOTAL (segundos)"
}

verificar_antigos
dump_postgresql
cp_arquivos
targz_todos
finalizacao

