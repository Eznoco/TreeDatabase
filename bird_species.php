<?php require('./header.php') ?>
<!--
----Created by Ezra Billings and Kieran Larrabee
-->

<?php
    $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
    $common_name = $_GET['common_name'];
    if (!isset($common_name)) {
        $common_name = "";
    }
    $scientific_name = isset($_GET['scientific_name']) ? $_GET['scientific_name'] : '';
    $action = $_GET['action'];
    if (!isset($action)) {
        if ($id == 0) {
            $action = 'none';
        } else {
            $action = "select";
        }
    }
    if ($action == 'select') {
        $query = 'select common_name, scientific_name from bird_species where id = ?';
        $stmt = mysqli_prepare($dbc, $query);
        mysqli_stmt_bind_param($stmt, "i", $id);
        mysqli_stmt_execute($stmt);
    
        $result = mysqli_stmt_get_result($stmt);
        $row = mysqli_fetch_assoc($result);
        if ($row) {
            $common_name = $row['common_name'];
            $scientific_name = $row['scientific_name'];
        }
    }
    if ($action == 'update') {
        if ($id > 0) {
            // UPDATE
            $query = "UPDATE bird_species SET common_name=?, scientific_name=? WHERE id=?";
            $stmt = mysqli_prepare($dbc, $query);
            mysqli_stmt_bind_param($stmt, "ssi", $common_name, $scientific_name, $id);
        } else {
            // INSERT
            $query = "INSERT INTO bird_species (common_name, scientific_name) VALUES (?, ?)";
            $stmt = mysqli_prepare($dbc, $query);
            mysqli_stmt_bind_param($stmt, "ss", $common_name, $scientific_name);
        }
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
        // Redirect back to list
        header("Location: bird_species_list.php");
        exit;
    }

    if ($action == 'delete') {
        // DELETE 
        $query = "delete from bird_species where id = ?";
        $stmt = mysqli_prepare($dbc, $query);
        mysqli_stmt_bind_param($stmt, "i", $id);
        mysqli_stmt_execute($stmt);
        mysqli_stmt_close($stmt);
        // Redirect back to list
        header("Location: bird_species_list.php");
        exit;
    }

?>

<h2><?= $id > 0 ? 'Edit Bird Species' : 'Add Bird Species' ?></h2>
<br>
<br>
<br>

<form action="bird_species.php">
    <input type="hidden" name="id" value="<?= $id ?>">
    <input type='hidden' name='action' value='update'>
    <table>
      <tr>
        <td>
          <label>Common Name:</label><br>
        </td>
        <td>
          <input type="text" name="common_name" value="<?= $common_name ?>" >
        </td>
      </tr>
  
      <tr>
        <td>
          <label>Scientific Name:</label><br>
        </td>
        <td>
          <input type="text" name="scientific_name" value="<?= $scientific_name ?>">
        </td>
      </tr>
    </table> 
    <p>
        <button type="submit">Save</button>
        <a href="bird_species_list.php">Cancel</a>
    </p>
</form>

<?php require('./footer.php') ?>
