<?php
session_start();
include "db.php";
$email = $_POST['email'];
$password = $_POST['password'];
$result = $conn->query("SELECT * FROM users WHERE email = '$email'");
$user = $result->fetch_assoc();
if ($user && password_verify($password, $user['password'])) {
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['role'] = $user['role'];
    echo "Login successful. Welcome " . $user['name'];
} else {
    echo "Invalid login!";
}
?>