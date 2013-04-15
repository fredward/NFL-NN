<?php
// this script is meant to update the summary: QB database
// get the AV, weighted AV of all players that played in the NFL
$connection = mysql_connect("127.0.0.1","root","ivy7paul");
if (!$connection)
{
	echo 'Could not connect: ' . mysql_error();
}
mysql_select_db("cs51project", $connection);
$result = mysql_query("SHOW COLUMNS FROM data");
if (!$result) {
    echo 'Could not run query: ' . mysql_error();
    exit;
}
if (mysql_num_rows($result) > 0) {
    while ($row = mysql_fetch_assoc($result)) {
        $type = $row['Type'];
        $fname = $row['Field'];
        $scaleName = "scale" . $fname;
        if (strpos($type,'double') !== false || strcasecmp("winstreak", $fname) == 0) {
		    echo "\ntrue for " . $row['Field'];
		    for ($yr=1970; $yr < 2013; $yr++) { 
				$sql2 = "SELECT $fname, id from data WHERE year = $yr";
				$result2 = mysql_query($sql2);
				$vals = array();
				while ($row2 = mysql_fetch_array($result2)) {
					array_push($vals, $row2[0]);
				}
				$max = max($vals);
				$min = min($vals);
				$spread = $max - $min;
				//echo "$fname ($yr):\nMax: $max, Min: $min\n\n";

				$result2 = mysql_query($sql2);
				while ($row2 = mysql_fetch_array($result2)) {
					$scaleValue = 0;
					if ($spread)
						$scaleValue = round((($row2[0] - $min) / $spread) * 100, 3);
					$sql3 = "UPDATE data SET " . $scaleName . " = " . $scaleValue . " WHERE id = " . $row2[1];
					echo "$sql3\n";
					if (!mysql_query($sql3,$connection))
					{			
						die('Error: ' . mysql_error());
					}
				}
			}
		}/*
    	$sql = "ALTER TABLE data ADD $fname $type";
    	echo "$sql\n";
		if (!mysql_query($sql,$connection))
		{			
			die('Error: ' . mysql_error());
		}*/
    }
}/*
for ($yr=1970; $yr < 2013; $yr++) { 

	$sql = "SELECT * from data WHERE year = $yr"
	for ($i=0; $i < ; $i++) { 
		# code...
	}
}*/

?>