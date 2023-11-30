CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the Plants table
CREATE TABLE Plants (
    plant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    type VARCHAR(250) NOT NULL,
    stage VARCHAR(250) NOT NULL,
    health VARCHAR(250) NOT NULL
);

-- Create the Workers table
CREATE TABLE Workers (
    worker_id INT AUTO_INCREMENT PRIMARY KEY,
    proficiency VARCHAR(50),
    name VARCHAR(255) NOT NULL
);

-- Create the Gardens table
CREATE TABLE Gardens (
    garden_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255),
    size DECIMAL(10, 2),
    capacity INT,
    soil VARCHAR(255),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create the Operates relationship table (One user can operate multiple gardens)
CREATE TABLE Operates (
    user_id INT,
    garden_id INT,
    PRIMARY KEY (user_id, garden_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (garden_id) REFERENCES Gardens(garden_id)
);

-- Create the Owns relationship table (One user can own multiple plants)
CREATE TABLE Owns (
    user_id INT,
    plant_id INT,
    PRIMARY KEY (user_id, plant_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

-- Create the Employs relationship table (Many users can employ many workers)
CREATE TABLE Employs (
    user_id INT,
    worker_id INT,
    PRIMARY KEY (user_id, worker_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id)
);

-- Create the Seeds relationship table (Plants can create more seeds among themselves)
CREATE TABLE Seeds (
    parent_plant_id INT,
    child_plant_id INT,
    PRIMARY KEY (parent_plant_id, child_plant_id),
    FOREIGN KEY (parent_plant_id) REFERENCES Plants(plant_id),
    FOREIGN KEY (child_plant_id) REFERENCES Plants(plant_id)
);

-- Create the Plants relationship table (Many workers can plant many plants)
CREATE TABLE Plants_Relationship (
    worker_id INT,
    plant_id INT,
    PRIMARY KEY (worker_id, plant_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id),
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

-- Create the Tends relationship table (Many workers can tend to many plants)
CREATE TABLE Tends (
    worker_id INT,
    plant_id INT,
    PRIMARY KEY (worker_id, plant_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id),
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

-- Create the Contains relationship table (Many gardens can contain many plants)
CREATE TABLE Contains (
    garden_id INT,
    plant_id INT,
    PRIMARY KEY (garden_id, plant_id),
    FOREIGN KEY (garden_id) REFERENCES Gardens(garden_id),
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

-- Create the Gardens relationship table (Many gardens are tended by many workers)
CREATE TABLE Gardens_Relationship (
    garden_id INT,
    worker_id INT,
    PRIMARY KEY (garden_id, worker_id),
    FOREIGN KEY (garden_id) REFERENCES Gardens(garden_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id)
);
