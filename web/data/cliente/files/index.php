<?php
include __DIR__.'../../../vendor/autoload.php';

Predis\Autoloader::register();
$client = new Predis\Client([
    'scheme' => 'tcp',
    'host'   => 'host.docker.internal',
    'port'   => 6379,
    'password' => 'SUASENHA'
]);

$GLOBALS['DIRS']= array();
function dirToArray($dir,$modpack) {
   $cdir = scandir($dir);
   foreach ($cdir as $key => $value){
      if (!in_array($value,array(".",".."))){
         if (is_dir($dir . DIRECTORY_SEPARATOR . $value)) {
            dirToArray($dir . DIRECTORY_SEPARATOR . $value, $modpack);
         } else {

            $hash = hash_file('sha1', $dir . "/" . $value);
            $size = filesize($dir . "/" . $value);
            $path = str_replace("files/".$modpack."/", "", $dir . "/" . $value);

            $url = "http://" . $_SERVER['HTTP_HOST'] ."/cliente/files/". $dir . "/" . $value;
            if (strpos($path, "libraries") !== false) {
               $type = "LIBRARY";
            } else if (strpos($path, "mods") !== false) {
               $type = "MOD";
            } else if (strpos($path, "versions") !== false) {
               $type = "VERIONSCUSTOM";
            } else {
               $type = "FILE";
            }
            $obj = array("path"=>$path, "size"=>$size, "sha1"=>$hash,"url"=>$url,"type"=>$type);
            array_push($GLOBALS['DIRS'], $obj);
         }
         
      }
   }

}

function getDirectory($identificador){
$json_file = file_get_contents('../launcher/config-launcher/modpacks.json');
$json = json_decode($json_file); // decode the JSON into an associative array
foreach ( $json as $e )
    {
       if($e->id == $identificador){
          return $e->directory;
       }
    }
    return null;
}

header("Content-Type: application/json; charset=UTF-8");
if (isset($_GET['modpack'])) {
$modpack = getDirectory($_GET['modpack']);
if($modpack == null){
   return;
}
$dir = "files/".$modpack;
$value = $client->get($_GET['modpack']);
if(!isset($value)){
   dirToArray($dir,$modpack);
   $resultado = json_encode($GLOBALS['DIRS'],JSON_UNESCAPED_SLASHES ) ;
   $client->set($_GET['modpack'], $resultado);
   $client->expire($_GET['modpack'], 3600);
   echo "[", $client->get($_GET['modpack']), "\"\"]";
}else{
   echo $client->get($_GET['modpack']);
}
}
?>