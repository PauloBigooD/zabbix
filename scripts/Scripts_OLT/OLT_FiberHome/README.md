# ![](https://iconape.com/wp-content/files/ix/351536/svg/351536.svg)

## FiberHome

- Neste repositório temos alguns scripts escritos em Python e PHP para auxiliar nas coletas das informações das ONU's / OLT FiberHome

## Habilitando coleta de potência via SNMP

    - Acesse o Setup da OLT via telnet e execute os seguintes comandos:
    - Para acessar como Admin use: enable 
    - Depois digite a senha, e em seguida execute os comandos:
    
      Admin# lll
      Admin(DEBUG_H)> set mib performance switch enable
      
    -Vai retornar a mensagem:
    
      set ok!
      
    -Em seguida use o comando a seguir para alternar o diretório atual:
    
      Admin# cd gponlinecard
      
    -E execute:
    
      Admin\gponline# set pon_traffic_sts switch traffic enable 1 0 opt enable 1 0 rtt enable 2 0
      
    -Vai retornar a mensagem:
    
      set ok!
      
    -Se em “lll” não funcionar esses comandos, entre em Device:
    -Para sair use exit
    -Acesse a OLT via telnet e execute os seguintes comandos:
    
      Admin# cd device
      Admin#device> set mib performance switch enable
      
    -Vai retornar a mensagem:
    
      set ok!
      
    -Em seguida vá em:
    
      Admin# cd gponlinecard
      
    -E execute:
    
      Admin\gponline# set pon_traffic_sts switch traffic enable 1 0 opt enable 1 0 rtt enable 2 0
    
    -Também deve retornar o OK:
    
      set ok!'
      
    -Por fim digite : 
    
      save
      
    -Para sair utilize: 
      
      cd .
      quit
