-- 🎯 Project Title
-- Job Portal Analytics & Applicant Tracking System (ATS)
CREATE DATABASE job_portal_ats;
USE job_portal_ats;

CREATE TABLE companies(
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    location VARCHAR(50),
    created_at DATE
);

CREATE TABLE jobs(
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    job_title VARCHAR(100),
    job_type VARCHAR(30),
    salary INT,
    posted_date DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE candidates(
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    experience_years INT,
    skills TEXT,
    registered_date DATE
);

CREATE TABLE applications(
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    candidate_id INT,
    applied_date DATE,
    current_status VARCHAR(30),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

CREATE TABLE application_status_history(
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT,
    status VARCHAR(30),
    status_date DATE,
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);

SHOW TABLES;

INSERT INTO companies(company_name, industry, location, created_at) VALUES
('TechNova', 'Software', 'Bangalore', '2023-01-10'),
('FinEdge', 'Finance', 'Mumbai', '2023-02-15'),
('HealthPlus', 'Healthcare', 'Pune', '2023-03-20'),
('EduSpark', 'EdTech', 'Hyderabad', '2023-04-05');

INSERT INTO jobs(company_id, job_title, job_type, salary, posted_date) VALUES
(1, 'Python Developer', 'Full-time', 800000, '2024-01-05'),
(1, 'Data Analyst', 'Intern', 300000, '2024-01-12'),
(2, 'Business Analyst', 'Full-time', 900000, '2024-02-01'),
(3, 'Data Engineer', 'Full-time', 1000000, '2024-02-10'),
(4, 'ML Engineer', 'Intern', 400000, '2024-03-01');

INSERT INTO candidates(full_name, email, experience_years, skills, registered_date) VALUES
('Amit Sharma', 'amit@gmail.com', 2, 'Python, SQL, Pandas', '2024-01-02'),
('Neha Verma', 'neha@gmail.com', 1, 'Excel, SQL, Power BI', '2024-01-08'),
('Rahul Patil', 'rahul@gmail.com', 3, 'Python, ML, TensorFlow', '2024-01-15'),
('Sneha Iyer', 'sneha@gmail.com', 0, 'Python, Statistics', '2024-02-01');

INSERT INTO applications(job_id, candidate_id, applied_date, current_status) VALUES
(1, 1, '2024-01-10', 'Applied'),
(2, 2, '2024-01-15', 'Applied'),
(3, 1, '2024-02-03', 'Applied'),
(5, 3, '2024-03-05', 'Applied'),
(4, 4, '2024-02-12', 'Applied');

INSERT INTO application_status_history(application_id, status, status_date) VALUES
(1, 'Applied', '2024-01-10'),
(1, 'Interview', '2024-01-20'),
(2, 'Applied', '2024-01-15'),
(3, 'Applied', '2024-02-03'),
(3, 'Rejected', '2024-02-18'),
(4, 'Applied', '2024-03-05'),
(4, 'Interview', '2024-03-15'),
(4, 'Hired', '2024-03-25');

SELECT * FROM companies;
SELECT * FROM jobs;
SELECT * FROM candidates;
SELECT * FROM applications;
SELECT * FROM application_status_history;

-- 1]Which company posted which job?
SELECT 
	c.company_name,
    j.job_title,
    j.job_type,
	j.salary 
FROM companies c
JOIN jobs j ON c.company_id = j.company_id;   

-- 2]Candidate applications with job title
SELECT
	ca.full_name,
    j.job_title,
    a.applied_date,
    a.current_status
FROM applications a 
JOIN candidates ca ON a.candidate_id = ca.candidate_id
join jobs j ON a.job_id = j.job_id;  

-- 3]Company-wise number of applications
SELECT
	c.company_name, COUNT(a.application_id) AS total_applications
FROM companies c
JOIN jobs j ON c.company_id = j.company_id
JOIN applications a ON j.job_id = a.job_id
GROUP BY c.company_name;    

-- 4]Average salary by company
SELECT 
	c.company_name, AVG(j.salary) AS avg_salary
FROM companies c
JOIN jobs j ON c.company_id = j.company_id
GROUP BY c.company_name;    

-- 5]Job demand (applications per job)
SELECT 
	j.job_title,
    COUNT(a.application_id) AS demand
FROM jobs j
LEFT JOIN applications a ON j.job_id = a.job_id
GROUP BY j.job_title;    

-- 6]Jobs with above-average salary
SELECT job_title, salary
FROM jobs
WHERE salary > (SELECT AVG(salary) FROM jobs);

-- 7] Candidates who applied to more than one job
SELECT full_name FROM candidates
WHERE candidate_id IN(
	SELECT candidate_id
    FROM applications
    GROUP BY candidate_id
    HAVING COUNT(job_id) > 1);
    
-- 8️] Hiring timeline (application → final status)
SELECT 
    a.application_id,
    MIN(h.status_date) AS applied_date,
    MAX(h.status_date) AS final_status_date,
    DATEDIFF(MAX(h.status_date), MIN(h.status_date)) AS hiring_days
FROM application_status_history h
JOIN applications a ON h.application_id = a.application_id
GROUP BY a.application_id;   

-- 9]Transactions(COMMIT)
START TRANSACTION;

UPDATE applications
SET current_status = 'Hired'
WHERE application_id = 1;

INSERT INTO application_status_history(application_id, status, status_date)
VALUES(1, 'Hired', CURDATE());

COMMIT;

-- 10]Transaction(ROLLBACK)
START TRANSACTION;

UPDATE applications
SET current_status = 'Rejected'
WHERE application_id = 2;

-- Intentional error(wrong column name)
INSERT INTO application_status_history (application_id, status_wrong, status_date)
VALUES (2, 'Rejected', CURDATE());

ROLLBACK;
-- To verify:
SELECT* FROM applications WHERE application_id = 2;
SELECT* FROM application_status_history WHERE application_id = 2; -- status did not change

-- 11]Transaction(SAVEPOINT)
START TRANSACTION;

SAVEPOINT before_update;

UPDATE applications
SET current_status = 'Applied'
WHERE application_id = 3;

-- something feels wrong
ROLLBACK TO before_update;

COMMIT;