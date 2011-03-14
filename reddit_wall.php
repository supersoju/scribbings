<?php
	error_reporting(0);
	$i = 0;
	while($i < 1) { //infinate loop
	$daysago = date("Y-m-d", mktime(0,0,0, date("m"), date("d")-2, date("Y")));
	
	$localdirectory = "/Users/USERNAME/Pictures/Backgrounds/reddit/"; //CHANGE THIS!!!
	
	$alreadyexist = array();
	
	if ($handle = opendir($localdirectory)) {
	    while (false !== ($file = readdir($handle))) {
	        if ($file != "." && $file != "..") {
	           $datemod = date("Y-m-d", filemtime($localdirectory.$file));
	           $alreadyexist[] = $file;
			   if($datemod == $daysago) {
			   		echo "Deleting Old File - ".$file."\n";
			   		unlink($localdirectory.$file);
			   };
			}
		}
		closedir($handle);
	}
	
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_URL, 'http://www.reddit.com/r/wallpapers/top/.json');
	$result = curl_exec($ch);
	$json_o=json_decode($result);
	$images = array("png", "jpg");
	foreach($json_o->data->children as $child)
		{ 
			if(in_array(substr($child->data->url, -3, 3),$images)) { 
				$fullfilename = $child->data->name.".".substr($child->data->url, -3, 3);
				if(in_array($fullfilename,$alreadyexist)) {
					echo "We already have ".$child->data->name.".".substr($child->data->url, -3, 3)."\n";
				} else {
					echo "Downloading - ".$fullfilename."\n";
					$stringData = file_get_contents($child->data->url);
					$myFile = $localdirectory.$fullfilename;
					$fh = fopen($myFile, 'a') or die("can't open file");
					fwrite($fh, $stringData);
					fclose($fh);
				};
			};
		};
	echo "Sleeping 1 hour\n";	
	sleep(3600);
	};
?>