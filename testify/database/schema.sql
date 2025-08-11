CREATE DATABASE IF NOT EXISTS test_report_db;
USE test_report_db;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Analyst', 'Viewer') DEFAULT 'Viewer',
    -- ADDED THE NEW COLUMNS FOR USER SETTINGS --
    data_view VARCHAR(50) DEFAULT 'Last 7 Days',
    notifications VARCHAR(50) DEFAULT 'All'
);

CREATE TABLE test_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    source_type ENUM('upload', 'api') NOT NULL,
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    filename VARCHAR(255) NULL,
    filesize VARCHAR(50) NULL,
    status VARCHAR(50) DEFAULT 'Completed',

    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE test_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT,
    product_name VARCHAR(255),
    test_id VARCHAR(100) NOT NULL,
    test_type VARCHAR(100),
    status ENUM('Pass', 'Fail', 'Pending') NOT NULL,
    execution_date DATE,
    frequency INT,
    tester VARCHAR(100),
    test_duration INT,
    FOREIGN KEY (report_id) REFERENCES test_reports(id)
);