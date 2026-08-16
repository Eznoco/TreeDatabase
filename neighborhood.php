<?php require('./header.php') ?>
<!--
----Created by Ezra Billings and Kieran Larrabee
-->

<?php
    $id = isset($_GET['id']) ? intval($_GET['id']) : 0; //gets id from url if it's there, otherwise saves id as 0
    $name = $_GET['name']; //grabs name from url
    if (!isset($name)) { //sets name to empty if no name in url
        $name = "";
    }
    $action = $_GET['action']; //gets action from url. We use action to decide which query to use
    if (!isset($action)) {
        if ($id == 0) {
            $action = 'none'; //no action if creating a new neighborhood. id is only 0 when adding a new neighborhood
        } else {
            $action = "select"; //otherwise set action to select
        }
    }
    if ($action == 'select') {
        $query = 'select name from neighborhood where id = ?';
        $stmt = mysqli_prepare($dbc, $query); //gets prepared statement for api
        mysqli_stmt_bind_param($stmt, "i", $id); //fills in question mark
        mysqli_stmt_execute($stmt); //submits the query
    
        $result = mysqli_stmt_get_result($stmt); //result hold the result table from query. Will only be one row since we're selecting by id
        $row = mysqli_fetch_assoc($result); //grabs a row from the result (this case its only one)
        if ($row) {
            $name = $row['name']; //assign the name to a variable so we can automatically put it into the text box
        }
    }
    if ($action == 'update') {
        if ($id > 0) {
            // UPDATE
            $query = "UPDATE neighborhood SET name=? WHERE id=?";
            $stmt = mysqli_prepare($dbc, $query);
            mysqli_stmt_bind_param($stmt, "si", $name, $id);
        } else {
            // INSERT
            $query = "INSERT INTO neighborhood (name) VALUES (?)";
            $stmt = mysqli_prepare($dbc, $query);
            mysqli_stmt_bind_param($stmt, "s", $name);
        }
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
        header("Location: neighborhood_list.php"); //We don't need any html here so we just redirect back to the list page
        exit;
    }

    if ($action == 'delete') {
        // DELETE 
        $query = "delete from neighborhood where id = ?";
        $stmt = mysqli_prepare($dbc, $query);
        mysqli_stmt_bind_param($stmt, "i", $id);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
        // Redirect back to list
        header("Location: neighborhood_list.php");
        exit;
    }

?>

<h2><?= $id > 0 ? 'Edit Neighborhood' : 'Add Neighborhood' ?></h2>
<br>
<br>
<br>

<form action="neighborhood.php"> <!-- action will tell which page to direct to when the form is submitted-->
    <!-- we need hidden inputs to add fields to url line -->
    <input type="hidden" name="id" value="<?= $id ?>">
    <input type='hidden' name='action' value='update'>
    <table>
      <tr>
        <td>
          <label>Name:</label><br>
        </td>
        <td>
          <input type="text" name="name" value="<?= $name ?>" >
        </td>
      </tr>
    </table> 
    <p>
        <button type="submit">Save</button>
        <a href="neighborhood_list.php">Cancel</a>
    </p>
</form>

<?php require('./footer.php') ?>
