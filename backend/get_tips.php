<?php
include "db.php";
$result = $conn->query("SELECT * FROM career_tips ORDER BY posted_at DESC");
while ($row = $result->fetch_assoc()) {
    echo "<h3>" . $row['title'] . "</h3>";
    echo "<p>" . $row['content'] . "</p><hr>";
}
?>