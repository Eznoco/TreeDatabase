<!DOCTYPE HTML>
<!--
----Created by Ezra Billings and Kieran Larrabee
-->
<html>
  <head>
    <link rel="stylesheet" href="tree.css">
  </head>
  <body>
    <div class="header">
      <h1><a href='index.html'>🏠</a> Tree Database</h1>
      <div class="navigation"> <!-- divisions of the page formatted by style sheet -->
        <a href="bird_species_list.php">Bird Species</a>
        <a href="tree_list.php">Trees</a>
        <a href="address_list.php">Addresses</a>
        <a href="neighborhood_list.php">Neighborhoods</a>
        <a href="tree_species_list.php">Tree Species</a>
      </div>
    </div>
    <div class="content"


<?php
  define('DB_USER', 'root');
  define('DB_PASSWORD', '');
  define('DB_HOST', 'localhost');
  define('DB_NAME', 'tree');

  ($dbc = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD,
                         DB_NAME))
    || die('Could not connect to MariaDB: '
           . mysqli_connect_error());
?>

  
