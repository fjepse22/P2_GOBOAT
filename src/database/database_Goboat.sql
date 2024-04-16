CREATE DATABASE Goboat;
-- version 1.0
-- Writen by: Frederik B. B. Jepsen
-- created: 12-04-2024
-- last modified: 13-04-3024
-- Last Modified by: Frederik B. B. Jepsen

-- This file creates the GoBOAT database with all the tables and restrictions.


-- Table with the boats
-- all bateries have a unique ID which is the serial number of the battery
CREATE TABLE Goboat.Boats(
Boat_ID char(8) PRIMARY KEY,
No_of_batteries INT NOT NULL
);

CREATE TABLE Goboat.Batteries(
Serial_Number char(8) PRIMARY KEY NOT NULL,
-- The time the battery was used in a boat the first time
First_used DATE,
-- The time the bateery is no longer used
Out_phased DATE DEFAULT NULL,
Out_phase_code CHAR(8) DEFAULT NULL,
-- The model of the battery
-- properties unique to the battey model is stored in another table
Battey_model_ID char(8),
-- state of health of the bateery (if calculated)
State_of_health INT DEFAULT 100,
-- how many times the battery have been char(8)ge
Cycle_counter INT DEFAULT 0,
-- how many times the battery have been char(8)ged from low % to full
Deep_cycle_counter INT DEFAULT 0
);

CREATE TABLE Goboat.Boats_batteries(
Row_ID INT PRIMARY KEY AUTO_INCREMENT,
Battery_ID CHAR(8) NOT NULL,
Boat_ID CHAR(8) NOT NULL,
Slot_number INT NOT NULL
);


CREATE TABLE Goboat.Battey_models(
Battey_model_ID CHAR(8) PRIMARY KEY NOT NULL,
Model_name VARCHAR(30),
Max_voltage FLOAT,
Voltage_schema VARCHAR(100),
Battery_type VARCHAR(20)
);

CREATE TABLE Goboat.Data_Boat(
-- ID for the data
Data_ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
Boat_ID  char(8),
Data_time DATETIME,
Lok_lat FLOAT,
Lok_long FLOAT,
Watt_hour FLOAT
);


-- subtable of Data_Boat
CREATE TABLE Goboat.Voltage(
Row_ID INT PRIMARY KEY AUTO_INCREMENT,
Data_ID INT,
Battery_ID CHAR(8),
Battery_temperature FLOAT,
Battery_voltage FLOAT
);



-- Here are alle the restrains defined (the primary and foreign key relatoins.

-- Restrains for the Boats table



-- restrains for the Batteries table
ALTER TABLE Goboat.Batteries
ADD CONSTRAINT batteries_FK
FOREIGN KEY (Battey_model_ID)
REFERENCES Battey_models (Battey_model_ID);


-- restrains for the Batteries table


-- contraints for the Battey_models table
ALTER TABLE Goboat.Battey_models
ADD CONSTRAINT Unique_bm_model_name
UNIQUE (Model_name); 


-- constraints for the Boats_batteries table

ALTER TABLE Goboat.Boats_batteries
ADD CONSTRAINT Boats_batteries_FK_boat
FOREIGN KEY (Boat_ID)
REFERENCES Boats (Boat_ID);

ALTER TABLE Goboat.Boats_batteries
ADD CONSTRAINT Boats_batteries_FK_battery
FOREIGN KEY (Battery_ID)
REFERENCES batteries (Serial_Number);

ALTER TABLE Goboat.Boats_batteries
ADD CONSTRAINT Boats_batteries_unique_slot
UNIQUE (Boat_ID,Slot_number);

ALTER TABLE Goboat.Boats_batteries
ADD CONSTRAINT Boats_batteries_unique_battery
UNIQUE (Battery_ID);

ALTER TABLE Goboat.Boats_batteries
-- Every boat needs at least one battery
ADD CONSTRAINT 
CHECK (Slot_number>=1);


-- constraints for the Data_Boat table

ALTER TABLE Goboat.Data_Boat
ADD CONSTRAINT Data_boat_FK
FOREIGN KEY (Boat_ID)
REFERENCES Boats (Boat_ID);

ALTER TABLE Goboat.Data_Boat
ADD CONSTRAINT Data_boat_unique
UNIQUE (Boat_ID,Data_time);


-- constraints for the Data_Voltage table

ALTER TABLE Goboat.Voltage
ADD CONSTRAINT Voltage_FK_Data_boat
FOREIGN KEY (Data_ID)
REFERENCES data_boat (Data_ID);

ALTER TABLE Goboat.Voltage
ADD CONSTRAINT Voltage_FK_Data_battery
FOREIGN KEY (Battery_ID)
REFERENCES Batteries (Serial_Number);

ALTER TABLE Goboat.Voltage
ADD CONSTRAINT Voltage_Unique
UNIQUE (Data_ID,Battery_ID);



