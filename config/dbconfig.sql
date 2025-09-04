CREATE DATABASE IF NOT EXISTS PlannedEvents;
USE PlannedEvents;

-- ---------------------
-- TABLES
-- ---------------------
CREATE TABLE IF NOT EXISTS Category
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Event
(
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    t_date      DATETIME NOT NULL,
    description VARCHAR(255),
    category    INT,
    FOREIGN KEY (category) REFERENCES Category(id)
);

-- ---------------------
-- SAMPLE DATA
-- ---------------------

-- Categories
INSERT IGNORE INTO Category (name) VALUES
('None'),
('Work'),
('Personal'),
('Health');

-- Events
-- Insert events only if they don't already exist (by name + t_date)
INSERT INTO Event (name, t_date, description, category)
SELECT * FROM (SELECT 'Doctor Appointment', '2025-09-05 10:30:00', 'Annual check-up', 4) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM Event WHERE name = 'Doctor Appointment' AND t_date = '2025-09-05 10:30:00'
) LIMIT 1;

INSERT INTO Event (name, t_date, description, category)
SELECT * FROM (SELECT 'Team Meeting', '2025-09-05 14:00:00', 'Discuss Q4 goals', 2) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM Event WHERE name = 'Team Meeting' AND t_date = '2025-09-05 14:00:00'
) LIMIT 1;

INSERT INTO Event (name, t_date, description, category)
SELECT * FROM (SELECT 'Birthday Party', '2025-09-07 19:00:00', 'At Anna''s place', 3) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM Event WHERE name = 'Birthday Party' AND t_date = '2025-09-07 19:00:00'
) LIMIT 1;

INSERT INTO Event (name, t_date, description, category)
SELECT * FROM (SELECT 'Grocery Shopping', '2025-09-03 17:00:00', 'Buy ingredients for dinner', 1) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM Event WHERE name = 'Grocery Shopping' AND t_date = '2025-09-03 17:00:00'
) LIMIT 1;

INSERT INTO Event (name, t_date, description, category)
SELECT * FROM (SELECT 'Gym Session', '2025-09-03 08:00:00', 'Leg day', 4) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM Event WHERE name = 'Gym Session' AND t_date = '2025-09-03 08:00:00'
) LIMIT 1;