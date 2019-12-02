<?php
/**
 *Plugin name: Skautis Mailgroups
 * Version 0.1
 * Author: Tomáš Kysela
 * License: The Unlicence
 */
$login_link = '';
class groups{
    public function init(){
        \add_shortcode('groups_main', [$this, 'groupsShortCode']);
    }

    private function input($data){
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }

    public function groupsShortCode() {
        $package = 'check login';
        $url = 'http://groups.tkysela.cz/check';
        $ch = curl_init($url);
        curl_setopt( $ch, CURLOPT_POST, 1);
        curl_setopt( $ch, CURLOPT_POSTFIELDS, $package);
        curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt( $ch, CURLOPT_MAXREDIRS, 5);
        curl_setopt( $ch, CURLOPT_HEADER, 0);
        curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);

        $response = curl_exec( $ch );
        if ($response != 'logged in') {
            $unit = $domain = '';
            if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                $unit = input($_POST['unit']);
                $domain = input($_POST['domain']);
                $page = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
            }
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
            if ($response != 'Busy') {
                header('Location: ' . $response, true, 307);
                die;
            }
            else {
                echo 'Please try again later';
            }
        }
        else {

        }
    }
}