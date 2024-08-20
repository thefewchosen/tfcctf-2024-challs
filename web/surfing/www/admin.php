<?php
$correctUsername = 'admin';
$correctPassword = 'admin';

if (isset($_GET['username']) && isset($_GET['password'])) {
    $username = $_GET['username'];
    $password = $_GET['password'];

    if ($username === $correctUsername && $password === $correctPassword) {
        echo 'Login successful. Welcome, admin! Flag is TFCCTF{18fd102247cb73e9f9acaa42801ad03cf622ca1c3689e4969affcb128769d0bc}';
    } else {
        echo 'Login failed. Incorrect admin username or admin password.';
    }
} else {
    echo 'Please provide both username and password.';
}
?>
