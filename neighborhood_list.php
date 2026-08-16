<?php require('./header.php'); ?>
<!--
----Created by Ezra Billings and Kieran Larrabee
-->

<h2>Neighborhoods</h2>

<?php $search = trim(isset($_GET['search']) ? $_GET['search'] : '');?>
<table>
  <tr>
    <td>
      <form action='neighborhood_list.php' method='GET' class='search-form'>
        <input type='text' name='search' value="<?= $search ?>">
        <button type='submit'>Search</button>
      </form>
    </td>
    <td>
      <a href='neighborhood.php' class='add_button'>Add Neighborhood</a>
    </td>
  </tr>
</table>

<?php
    $query = "select id, name
              from neighborhood
             ";
    if ($search !== '') { //if search is not empty
        $query = $query . ' where name like ?'; //add the where clause to the query
        $like = "%" . $search . "%"; 
        $stmt = mysqli_prepare($dbc, $query); //prepars the query for the api
        mysqli_stmt_bind_param($stmt, "s", $like); //fills in the question marks.
    } else {
        $stmt = mysqli_prepare($dbc, $query); //prepares the query without the where clause
    }
    mysqli_stmt_execute($stmt); //runs the query
    $result = mysqli_stmt_get_result($stmt); //assigns the results to result variable. result contains everything returned by the executed query.
    if ($result) {
?>

<table>
  <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>
  <?php while ($row = mysqli_fetch_assoc($result)) { //grabs row from database result ?>
      <tr>
        <td><?= $row['id'] ?></td>
        <td><?= $row['name'] ?></td>
        <td>
          <a href="neighborhood.php?id=<?= $row['id'] ?>">✏️</a> <!-- id is added to url as page is created --> 
        </td>
        <td>
          <a href="neighborhood.php?action=delete&id=<?= $row['id'] ?>">🗑️</a>
        </td>
      </tr>
  <?php } ?>
</table>
<?php
    }
?> 

<?php require('./footer.php'); ?>
