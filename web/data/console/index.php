<?php

$interval = 500; //how often it checks the log file for changes, min 100
$textColor = ""; //use CSS color
// Don't have to change anything bellow
if(!$textColor) $textColor = "white";



if($interval < 100)  $interval = 100;

if(isset($_GET['getLog']) && isset($_GET['servidor'])){
	if(!file_exists($_GET['servidor'])){
		return;
	}
	echo file_get_contents($_GET['servidor']);
}else{
?>
<html>
	<title>Log de <?php echo $_GET['servidor']; ?> </title>
	<style>
		@import url(http://fonts.googleapis.com/css?family=Ubuntu);
		body{
			background-color: black;
			color: <?php echo $textColor; ?>;
			font-family: 'Ubuntu', sans-serif;
			font-size: 16px;
			line-height: 20px;	
		}
		h4{
			font-size: 18px;
			line-height: 22px;
			color: #353535;
		}
		#log {
			position: relative;
			top: -34px;
		}
		#scrollLock{
			width:40px;
			height: 40px;
			overflow:visible;
		}
	</style>
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js" type="text/javascript"></script>
	<script>
		
		setInterval(readLogFile, <?php echo $interval; ?>);
		
		window.load = readLogFile; 
		var pathname = window.location.pathname;
		var queryString = window.location.search;
		var scrollLock = true;
		
		$(document).ready(function(){
			$('.disableScrollLock').click(function(){
				$("html,body").clearQueue()
				$(".disableScrollLock").hide();
				$(".enableScrollLock").show();
				scrollLock = false;
			});
			$('.enableScrollLock').click(function(){
				$("html,body").clearQueue()
				$(".enableScrollLock").hide();
				$(".disableScrollLock").show();
				scrollLock = true;
			});
		});
		function readLogFile(){
			
			var urlParams = new URLSearchParams(queryString);
			var servidor = urlParams.get('servidor')
			var path_log = `../servidores/${servidor}/logs/latest.log`
			$.get(pathname, { getLog : "true", servidor: path_log }, function(data) {
				data = data.replace(new RegExp("\n", "g"), "<br />");
		        $("#log").html(data);
		        
		        if(scrollLock == true) { $('html,body').animate({scrollTop: $("#scrollLock").offset().top}, <?php echo $interval; ?>) };
		    });
		}
	</script>
	<body>
		<div id="log"></div>
		<div id="scrollLock"> <input class="disableScrollLock" type="button" value="Disable Scroll Lock" /> <input class="enableScrollLock" style="display: none;" type="button" value="Enable Scroll Lock" /></div>

	</body>
</html>
<?php  } ?>