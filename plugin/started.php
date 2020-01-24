<?php
$data = $_POST;
echo ('running');
$url = 'http://groups.tkysela.cz/start';
$ch = curl_init($url);
curl_setopt( $ch, CURLOPT_POST, 1);
curl_setopt( $ch, CURLOPT_POSTFIELDS, $data);
curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt( $ch, CURLOPT_MAXREDIRS, 5);
curl_setopt( $ch, CURLOPT_HEADER, 0);
curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec( $ch );
echo ('finished');
sleep(1);
header('Location: ' . $response, true, 307);
die;