-- init_db.sql

CREATE TABLE testcases (
    id SERIAL PRIMARY KEY,
    test_case_name VARCHAR(255) NOT NULL,
    estimate_time VARCHAR(50),
    module VARCHAR(100),
    priority VARCHAR(50),
    status VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO testcases (test_case_name, estimate_time, module, priority, status)
VALUES 
('Test Case 1', '5 Minutes', 'Onboarding', 'Low', 'Pending'),
('Test Case 2', '5 Minutes', 'User Log In', 'Medium', 'Pending'),
('Test Case 3', '5 Minutes', 'Password', 'High', 'Pending');
