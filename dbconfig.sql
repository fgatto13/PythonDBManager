DROP DATABASE IF EXISTS PlannedEvents;
CREATE DATABASE IF NOT EXISTS PlannedEvents;
USE PlannedEvents;

-- ---------------------
-- TABLES
-- ---------------------
CREATE TABLE Category
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Event
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
INSERT INTO Category (name) VALUES
('None'),
('Work'),
('Personal'),
('Health');

-- Events
INSERT INTO Event (name, t_date, description, category) VALUES
('Doctor Appointment', '2025-09-05 10:30:00', 'Annual check-up', 4),
('Team Meeting', '2025-09-05 14:00:00', 'Discuss Q4 goals', 2),
('Birthday Party', '2025-09-07 19:00:00', 'At Anna\'s place', 3),
('Grocery Shopping', '2025-09-03 17:00:00', 'Buy ingredients for dinner', 1),
('Gym Session', '2025-09-03 08:00:00', 'Leg day', 4);
