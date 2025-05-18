CREATE DATABASE IF NOT EXISTS stress_db;
USE stress_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
    phone_number VARCHAR(15) UNIQUE NOT NULL      -- User's phone number (unique)

);

-- Create stress_data table with a foreign key to users table
CREATE TABLE IF NOT EXISTS stress_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mood VARCHAR(50) NOT NULL,
    sleep_hours INT NOT NULL,
    coffee INT NOT NULL, 
    water_intake INT NOT NULL,
    work_hours INT NOT NULL,
    stress_level FLOAT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Optionally, create an index on user_id for faster lookups
CREATE INDEX idx_user_id ON stress_data(user_id);
