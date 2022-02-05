<?php
namespace App\Services;

class RedisService
    {
       
       public static $client = null;


       public static function Init($client){

       if(self::$client == null){

        self::$client = $client;
       
         }

    }
    }