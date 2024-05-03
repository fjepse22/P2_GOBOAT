DROP DATABASE goboatv2;
CREATE DATABASE goboatv2;
-- version 1.0
-- Writen by: Frederik B. B. Jepsen
-- created: 12-04-2024
-- last modified: 13-04-3024
-- Last Modified by: Frederik B. B. Jepsen

-- This file creates the GoBOAT database with all the tables and restrictions.


-- Table with the boats
-- all bateries have a unique ID which is the serial number of the battery


CREATE TABLE goboatv2.boats(
boat_ID char(8) PRIMARY KEY,
total_slots INT NOT NULL
);

CREATE TABLE goboatv2.batteries(
bat_ID char(8) PRIMARY KEY NOT NULL,
-- The time the battery was used in a boat the first time
first_used DATE,
-- The time the bateery is no longer used
outphased DATE DEFAULT NULL,
outphase_code CHAR(8) DEFAULT NULL,
-- The model of the battery
-- properties unique to the battey model is stored in another table
model_ID char(8),
-- state of health of the bateery (if calculated)
State_of_health INT DEFAULT 100,
-- how many times the battery have been char(8)ge
Cycle_counter INT DEFAULT 0,
-- how many times the battery have been char(8)ged from low % to full
Deep_cycle_counter INT DEFAULT 0
);

CREATE TABLE goboatv2.boat_conf(
row_ID INT PRIMARY KEY AUTO_INCREMENT,
bat_ID CHAR(8) NOT NULL,
boat_ID CHAR(8) NOT NULL,
slot_no INT NOT NULL
);


CREATE TABLE goboatv2.battery_models(
model_ID CHAR(8) PRIMARY KEY NOT NULL,
model_name VARCHAR(30),
max_voltage FLOAT,
voltage_schema VARCHAR(100),
battery_type VARCHAR(20)
);

CREATE TABLE goboatv2.boat_log(
-- ID for the data
data_ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
boat_ID  char(8),
data_time DATETIME,
lok_lat FLOAT,
lok_long FLOAT,
watt FLOAT
);


-- subtable of boat_log
CREATE TABLE goboatv2.battery_log(
row_ID INT PRIMARY KEY AUTO_INCREMENT,
data_ID INT,
bat_ID CHAR(8),
voltage FLOAT,
temperature FLOAT
);



-- Here are alle the restrains defined (the primary and foreign key relatoins.

-- Restrains for the boats table
ALTER TABLE goboatv2.boats
ADD CONSTRAINT re_boats_slot
CHECK (total_slots>=1);



-- restrains for the batteries table
ALTER TABLE goboatv2.batteries
ADD CONSTRAINT batteries_FK
FOREIGN KEY (model_ID)
REFERENCES battery_models (model_ID);


-- restrains for the batteries table


-- contraints for the battery_models table
ALTER TABLE goboatv2.battery_models
ADD CONSTRAINT Unique_model_name
UNIQUE (model_name); 


-- constraints for the boat_conf table

ALTER TABLE goboatv2.boat_conf
ADD CONSTRAINT boat_conf_FK_boat
FOREIGN KEY (boat_ID)
REFERENCES boats (boat_ID);

ALTER TABLE goboatv2.boat_conf
ADD CONSTRAINT boat_conf_FK_battery
FOREIGN KEY (bat_ID)
REFERENCES batteries (bat_ID);

ALTER TABLE goboatv2.boat_conf
ADD CONSTRAINT boat_conf_unique_slot
UNIQUE (boat_ID,slot_no);

ALTER TABLE goboatv2.boat_conf
ADD CONSTRAINT boat_conf_unique_battery
UNIQUE (Bat_ID);

ALTER TABLE goboatv2.boat_conf
-- slot number goes from 1 and onwords
ADD CONSTRAINT boat_conf_number
CHECK (slot_no>=1);


-- constraints for the boat_log table

ALTER TABLE goboatv2.boat_log
ADD CONSTRAINT boat_log_FK
FOREIGN KEY (boat_ID)
REFERENCES boats (boat_ID);

ALTER TABLE goboatv2.boat_log
ADD CONSTRAINT boat_log_unique
UNIQUE (boat_ID,Data_time);


-- constraints for the battery_log table

ALTER TABLE goboatv2.battery_log
ADD CONSTRAINT battery_log_FK_boat_log
FOREIGN KEY (Data_ID)
REFERENCES boat_log (Data_ID);

ALTER TABLE goboatv2.battery_log
ADD CONSTRAINT battery_log_FK_Data_battery
FOREIGN KEY (bat_ID)
REFERENCES batteries (bat_ID);

ALTER TABLE goboatv2.battery_log
ADD CONSTRAINT battery_log_Unique
UNIQUE (Data_ID,bat_ID);
