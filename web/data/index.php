<?php

    if ($handle = opendir('./downloads')) {

      while (false !== ($entry = readdir($handle))) {

        if ($entry != "." && $entry != "..") {

        echo '<a href="/prac/admin/'.$entry.'"' .'download="'.$entry.'">'.$entry.'</a>'.'<br>';       
        }
      }
    }
    closedir($handle);

?>