#!/usr/bin/php

<?php
    //Contato: pauloeduardodojunior19gmail.com;
    //apt-get install -y php-snmp;
	error_reporting(E_ALL ^ E_WARNING);
	snmp_set_quick_print(TRUE);
	$EMS   = '172.16.81.2';
	$UN    = 'logica';
	$PWD   = 'logica.2017';
	$OLTID = "{$argv[5]}";
	$SLOT  = snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.2.{$argv[1]}");
	$PON   = snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.3.{$argv[1]}");
	$MAC   = str_replace('"', "", snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.10.{$argv[1]}"));
	$FP    = stream_socket_client("tcp://{$EMS}:3337", $errno, $errstr, 5);
	//echo "$errstr ($errno)";
   	//die();
	while (!$FP){
	echo "teste";
    	sleep(1);
		$FP    = stream_socket_client("tcp://{$EMS}:3337", $errno, $errstr, 5);
		//$FP    = stream_socket_client("tcp://{$EMS}:5101", $errno, $errstr, 5);
                //stream_set_blocking($FP, FALSE);
	}
    //echo("OK");
    //die();
    fwrite($FP, "LOGIN:::CTAG::UN={$UN},PWD={$PWD};\n");
    $buffer = '';
    $datebefore = time();
    while (true) {
            $c = fread($FP, 1);
	    //echo $c;
            //echo 'teste';
	    //die();
            $buffer.=$c;
            if ((time()-$datebefore > 2)) {
		fclose($FP);
                $FP = stream_socket_client("tcp://{$EMS}:3337", $errno, $errstr, 5);
		while (!$FP){
                        sleep(1);
                        $FP    = stream_socket_client("tcp://{$EMS}:3337", $errno, $errstr, 5);
	        }
		fwrite($FP, "LOGIN:::CTAG::UN={$UN},PWD={$PWD};\n");
                $datebefore = time();
            }
            if ($c == ';') {
                break;
            }
    usleep(5000);
    }
    //echo "OLTID= $OLTID \n SLOT=$SLOT \n PON=$PON \n MAC=$MAC \n";
    //die();
    //echo "$errstr($errno)";
    fwrite($FP, "LST-OMDDM::OLTID={$OLTID},PONID=1-1-{$SLOT}-{$PON},ONUIDTYPE=MAC,ONUID={$MAC}:CTAG::;\n");
    $buffer = '';
    while (true) {
        $c = fread($FP, 1);
        //echo $c;
	$buffer.=$c;
        if ($c == ';')
            break;
    }
    $ret = explode("\n", $buffer);                                  
    $ret = explode("\t", $ret[11]);                                                                        
    fwrite($FP, "LOGOUT:::CTAG::;\n");
    fclose($FP);            
    if ($ret[1] == '--') { 
        $ret[1] = 0;              
    }                              
    //echo($ret[1]);                                                                                       
    $ret[1] = str_replace(',' , '.', $ret[1]);
    echo("$ret[1] \n");    

?>
