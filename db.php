<?php 
$server = "localhost:3308";
$username = "root";
$password = "";
$dbname = "eco_tourism";

$conn = new mysqli($server,$username,$password, $dbname);
if(!$conn)
{
    echo "Error!: {$conn->connect_error}";
}

?>