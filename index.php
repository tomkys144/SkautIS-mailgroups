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
        \add_shortcode('groups', [$this, 'groupsShortCode']);
    }

    private function input($data){
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }

    public function groupsShortCode() {
        $unit = $domain = '';
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $unit = input($_POST['unit']);
            $domain = input($_POST['domain']);
        }
        $url = 'http://groups.tkysela.cz/setup';
        $package = array('unit' => $unit, 'domain' => $domain);
        $data = json_encode($package);
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data)
            )
        );
        $context  = stream_context_create($options);
        $result = file_get_contents($url, false, $context);
        var_dump($result);
    }
}