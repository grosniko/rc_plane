<?php 

$input  = $_POST['input'];

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($socket, "127.0.0.1", 12345);
socket_write($socket, $input);


if(socket_last_error($socket)==32){
        try{
             exec("python3 control.py");
             sleep(3);
             socket_write($socket, $input);
             // echo "on";
        }
        catch(Exception $e){
                echo "Python ERROR!";
        }
} else {
        $response = socket_read($socket, 1024);
        socket_close($socket);
        echo $response;
}


?>