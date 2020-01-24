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
        \add_shortcode('is_groups', [$this, 'groupsShortCode']);
    }


    private function input($data) {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }


    public function groupsShortCode() {
        $url = 'http://groups.tkysela.cz/login';
        $ch = curl_init($url);
        curl_setopt( $ch, CURLOPT_POST, 1);
        curl_setopt( $ch, CURLOPT_POSTFIELDS, 'check login');
        curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt( $ch, CURLOPT_MAXREDIRS, 5);
        curl_setopt( $ch, CURLOPT_HEADER, 0);
        curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);

        $response = curl_exec( $ch );
        if ($response != 'started') {
            include 'notstarted.php';
        }
        elseif ($response == 'started') {
            include 'started.php';
        }
    }
}
