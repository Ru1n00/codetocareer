<?php
session_start();
include "db.php";
if ($_SESSION['role'] != 'admin') {
    echo "Access denied.";
    exit;
}
$title = $_POST['title'];
$content = $_POST['content'];
$sql = "INSERT INTO career_tips (title, content) VALUES ('$title', '$content')";
if ($conn->query($sql)) {
    echo "Tip posted.";
} else {
    echo "Error: " . $conn->error;
}
?>