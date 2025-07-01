CREATE DATABASE IF NOT EXISTS mydatabase;
CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'appuser'@'%';
FLUSH PRIVILEGES;

-- Create messages table
USE mydatabase;
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);