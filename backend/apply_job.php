<?php
session_start();
include "db.php";
$user_id = $_SESSION['user_id'];
$job_title = $_POST['job_title'];
$company = $_POST['company'];
$resume = $_POST['resume'];
$sql = "INSERT INTO jobs (user_id, job_title, company, resume) 
        VALUES ('$user_id', '$job_title', '$company', '$resume')";
if ($conn->query($sql)) {
    echo "Job applied successfully.";
} else {
    echo "Error: " . $conn->error;
}
?>