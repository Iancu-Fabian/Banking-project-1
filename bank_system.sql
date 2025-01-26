-- Create Database
CREATE DATABASE IF NOT EXISTS bank_system;
USE bank_system;

-- Create Clients Table
CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20)
);

-- Create Loans Table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    interest_rate DECIMAL(4, 2) NOT NULL,
    start_date DATE NOT NULL
);

-- Create Intermediary Table for M:N Relationship
CREATE TABLE contracts (
    client_id INT,
    loan_id INT,
    loan_date DATE NOT NULL,
    PRIMARY KEY (client_id, loan_id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE
);

INSERT INTO clients (first_name, last_name, email, phone_number) VALUES
    ('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
    ('Jane', 'Smith', 'jane.smith@example.com', '234-567-8901'),
    ('Robert', 'Brown', 'robert.brown@example.com', '345-678-9012'),
    ('Emily', 'Clark', 'emily.clark@example.com', '456-789-0123'),
    ('Michael', 'Davis', 'michael.davis@example.com', '567-890-1234'),
    ('Sarah', 'Wilson', 'sarah.wilson@example.com', '678-901-2345');

-- Insert sample data into Loans table
INSERT INTO loans (loan_type, amount, interest_rate, start_date) VALUES
    ('Personal Loan', 5000.00, 5.50, '2023-01-15'),
    ('Auto Loan', 15000.00, 4.25, '2023-02-20'),
    ('Mortgage', 250000.00, 3.75, '2023-03-10'),
    ('Business Loan', 100000.00, 6.00, '2023-04-05'),
    ('Student Loan', 20000.00, 4.00, '2023-05-25'),
    ('Home Equity Loan', 75000.00, 5.00, '2023-06-15');

-- Insert sample data into contracts table to establish relationships
INSERT INTO contracts (client_id, loan_id, loan_date) VALUES
    (1, 1, '2023-01-16'),
    (1, 2, '2023-02-21'),
    (2, 3, '2023-03-11'),
    (3, 4, '2023-04-06'),
    (4, 5, '2023-05-26'),
    (5, 6, '2023-06-16'),
    (6, 1, '2023-06-20'),
    (2, 2, '2023-02-23'),
    (3, 1, '2023-03-15'),
    (4, 3, '2023-05-11');