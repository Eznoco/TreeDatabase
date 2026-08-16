<?php require('./header.php'); ?>
<!--
----Created by Ezra Billings and Kieran Larrabee
-->

<h2>Bird Species</h2>

<?php $search = trim(isset($_GET['search']) ? $_GET['search'] : '');?>
<table>
  <tr>
    <td>
      <form action='bird_species_list.php' method='GET' class='search-form'>
        <input type='text' name='search' value="<?= $search ?>">
        <button type='submit'>Search</button>
      </form>
    </td>
    <td>
      <a href='bird_species.php' class='add_button'>Add Bird Species</a>
    </td>
  </tr>
</table>

<?php
    $query = "select id, common_name, scientific_name
              from bird_species
             ";
    if ($search !== '') {
        $query = $query . ' where common_name like ? or scientific_name like ?';    
        $like = "%" . $search . "%";
        $stmt = mysqli_prepare($dbc, $query);
        mysqli_stmt_bind_param($stmt, "ss", $like, $like); //fills in the question marks
    } else {
        $stmt = mysqli_prepare($dbc, $query);
    }
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    if ($result) {
?>

<table>
  <tr>
    <th>ID</th>
    <th>Common Name</th>
    <th>Scientific Name</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>
  <?php while ($row = mysqli_fetch_assoc($result)) { ?>
      <tr>
        <td><?= $row['id'] ?></td>
        <td><?= $row['common_name'] ?></td>
        <td><?= $row['scientific_name'] ?></td>
        <td>
          <a href="bird_species.php?id=<?= $row['id'] ?>">✏️</a>
        </td>
        <td>
          <a href="bird_species.php?action=delete&id=<?= $row['id'] ?>">🗑️</a>
        </td>
      </tr>
  <?php } ?>
</table>
<?php
    }
?> 

<?php require('./footer.php'); ?>
