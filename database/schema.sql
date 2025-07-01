-- Database Schema for AWS Three-Tier Backend
-- This file contains the database structure for the messages application

CREATE DATABASE mydatabase;
USE mydatabase;

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);