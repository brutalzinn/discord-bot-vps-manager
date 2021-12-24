<?php
$ignorar = array("index.php",".gitkeep");

    if ($handle = opendir('./')) {

      while (false !== ($entry = readdir($handle))) {

        if ($entry != "." && $entry != ".." && !in_array( $entry, $ignorar)) {

        echo '<a href="/data/downloads/'.$entry.'"' .'download="'.$entry.'">'.$entry.'</a>'.'<br>';       
        }
      }
    }
    closedir($handle);

?>