#!/usr/bin/php
<?php
	error_reporting(E_ALL ^ E_WARNING);
	snmp_set_quick_print(TRUE);
	$EMS   = '0.0.0.0';        // Endereço IP do UNM2000/ANM2000
	$UN    = '*******';        // Usuário de acesso ao UNM2000/ANM2000
	$PWD   = '*******';        // Senha de acesso ao UNM2000/ANM2000
	$OLTID = "{$argv[5]}";
	$SLOT  = snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.2.{$argv[1]}");
	$PON   = snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.3.{$argv[1]}");
	$MAC   = str_replace('"', "", snmp2_get("{$argv[3]}", "{$argv[4]}", ".1.3.6.1.4.1.5875.800.3.10.1.1.10.{$argv[1]}"));
	$FP    = stream_socket_client("tcp://{$EMS}:3337", $errno, $errstr, 5);
	$FNAME    = stream_socket_client("tcp://{$EMS}:3337", $errnoN, $errstrN, 5);
	while (!$FNAME){
		sleep(1);
		$FNAME    = stream_socket_client("tcp://{$EMS}:3337", $errnoN, $errstrN, 5);
    		//stream_set_blocking($FP, FALSE);
	}

    fwrite($FP, "LOGIN:::CTAG::UN={$UN},PWD={$PWD};\n");
    $buffer = '';
    $datebefore = time();
    while (true) {
            $c = fread($FP, 1);
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
    
    fwrite($FNAME, "LOGIN:::CTAG::UN={$UN},PWD={$PWD};\n");
    $bufferName = '';
    $datebeforeName = time();
    while (true) {
            $cName = fread($FNAME, 1);
            $bufferName.=$cName;
            if ((time()-$datebeforeName > 2)) {
                fclose($FNAME);
                $FNAME = stream_socket_client("tcp://{$EMS}:3337", $errnoN, $errstrN, 5);
                while (!$FNAME){
                        sleep(1);
                        $FNAME    = stream_socket_client("tcp://{$EMS}:3337", $errnoN, $errstrN, 5);
                }
                fwrite($FNAME, "LOGIN:::CTAG::UN={$UN},PWD={$PWD};\n");
                $datebeforeName = time();
            }
            if ($cName == ';') {
                break;
            }
    usleep(5000);
    }

    fwrite($FP, "LST-OMDDM::OLTID={$OLTID},PONID=1-1-{$SLOT}-{$PON},ONUIDTYPE=MAC,ONUID={$MAC}:CTAG::;\n");
    $buffer = '';
    while (true) {
        $c = fread($FP, 1);
        $buffer.=$c;
        if ($c == ';')
            break;
    }
    
    fwrite($FNAME, "LST-ONU::OLTID={$OLTID},PONID=1-1-{$SLOT}-{$PON},ONUIDTYPE=MAC,ONUID={$MAC}:CTAG::;\n");
    $bufferName = '';
    while (true) {
        $cName = fread($FNAME, 1);
        $bufferName.=$cName;
        if ($cName == ';')
            break;
    }


    $name = explode("\n", $bufferName);
    $name = explode("\t", $name[11]);
    fwrite($FNAME, "LOGOUT:::CTAG::;\n");
    fclose($FNAME);
    if ($name[1] == '--') {
        $name[1] = 0;
    }
    echo("Cliente : $name[3]\n");

    $ret = explode("\n", $buffer);
    $ret = explode("\t", $ret[11]);
    fwrite($FP, "LOGOUT:::CTAG::;\n");
    fclose($FP);
    if ($ret[1] == '--') {
	$ret[1] = 0;
    }

    echo("Potência Recebida : $ret[1] dBm\n");

?>
