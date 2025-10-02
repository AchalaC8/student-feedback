CREATE DATABASE IF NOT EXISTS feed;
USE feed;

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(255),
    student_name VARCHAR(255),
    usn VARCHAR(50),
    email VARCHAR(255),
    resource_person VARCHAR(255),
    topic VARCHAR(255),
    rating INT,
    feedback TEXT
);

-- Session table
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(255),
    resource_person VARCHAR(255),
    topic VARCHAR(255)
);
