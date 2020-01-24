<?php
if (isset($_POST['submit'])) {
    $unit = $_REQUEST['unit'];
    $domain = $_REQUEST['domain'];
}

$page = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";


$url = 'http://groups.tkysela.cz/setup';
$package = array('unit' => $unit, 'domain' => $domain, 'page' => $page);
$ch = curl_init($url);
curl_setopt( $ch, CURLOPT_POST, 1);
curl_setopt( $ch, CURLOPT_POSTFIELDS, $package);
curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt( $ch, CURLOPT_MAXREDIRS, 5);
curl_setopt( $ch, CURLOPT_HEADER, 0);
curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec( $ch );

header('Location: ' . $response, true, 307);