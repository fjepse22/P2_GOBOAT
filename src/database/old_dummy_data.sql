-- version 1.0
-- Writen by: Frederik B. B. Jepsen
-- created: 12-04-2024
-- last modified:
-- Last Modified by:

-- This is dummy data for the old database
-- This file adds dummy data for boats, batteries, battery models and the boats battery tables
-- This data is needed in order to insert data about the boat's battery state.


-- dummy battery model
INSERT INTO Goboat.Battey_models (Battey_model_ID,Model_name,Max_voltage,Voltage_schema,Battery_type)
VALUES ('lit_m1','litiumion model 1','12','volt_skema','LitiumIon');


-- Dummy batteriries for the boats
INSERT INTO Goboat.Batteries 	(Serial_Number,First_used,Battey_model_ID)
VALUES 
-- ('nobat','2000-01-01',NULL),
('bat11','2024-04-07','lit_m1'),
('bat12','2024-04-07','lit_m1'),
('bat13','2024-04-07','lit_m1'),
('bat14','2024-04-07','lit_m1'),
('bat15','2024-04-07','lit_m1'),
('bat16','2024-04-07','lit_m1'),
('bat17','2024-04-07','lit_m1'),
('bat18','2024-04-07','lit_m1'),
('bat20','2024-04-07','lit_m1'),
('bat21','2024-04-07','lit_m1'),
('bat22','2024-04-07','lit_m1'),
('bat23','2024-04-07','lit_m1'),
('bat24','2024-04-07','lit_m1'),
('bat25','2024-04-07','lit_m1'),
('bat26','2024-04-07','lit_m1'),
('bat27','2024-04-07','lit_m1'),
('bat28','2024-04-07','lit_m1'),
('bat30','2024-04-07','lit_m1'),
('bat31','2024-04-07','lit_m1'),
('bat32','2024-04-07','lit_m1'),
('bat33','2024-04-07','lit_m1'),
('bat34','2024-04-07','lit_m1'),
('bat35','2024-04-07','lit_m1'),
('bat36','2024-04-07','lit_m1'),
('bat37','2024-04-07','lit_m1'),
('bat38','2024-04-07','lit_m1'),
('bat40','2024-04-07','lit_m1'),
('bat41','2024-04-07','lit_m1'),
('bat42','2024-04-07','lit_m1'),
('bat43','2024-04-07','lit_m1'),
('bat44','2024-04-07','lit_m1'),
('bat45','2024-04-07','lit_m1'),
('bat46','2024-04-07','lit_m1'),
('bat47','2024-04-07','lit_m1'),
('bat48','2024-04-07','lit_m1'),
('bat50','2024-04-07','lit_m1'),
('bat51','2024-04-07','lit_m1'),
('bat52','2024-04-07','lit_m1'),
('bat53','2024-04-07','lit_m1'),
('bat54','2024-04-07','lit_m1'),
('bat55','2024-04-07','lit_m1'),
('bat56','2024-04-07','lit_m1'),
('bat57','2024-04-07','lit_m1'),
('bat58','2024-04-07','lit_m1')
;


--  data for the boat table

INSERT INTO Goboat.Boats (boat_ID,No_of_batteries)
VALUES 
('boat1',8),
('boat2',8),
('boat3',8),
('boat4',8),
('boat5',8),
('boat6',8)
;

-- Data for the boats

INSERT INTO Goboat.Boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat11','boat1',1),
('bat12','boat1',2),
('bat13','boat1',3),
('bat14','boat1',4),
('bat15','boat1',5),
('bat16','boat1',6),
('bat17','boat1',7),
('bat18','boat1',8)
;

INSERT INTO Goboat.Boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat21','boat2',1),
('bat22','boat2',2),
('bat23','boat2',3),
('bat24','boat2',4),
('bat25','boat2',5),
('bat26','boat2',6),
('bat27','boat2',7),
('bat28','boat2',8)
;

INSERT INTO Goboat.Boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat31','boat3',1),
('bat32','boat3',2),
('bat33','boat3',3),
('bat34','boat3',4),
('bat35','boat3',5),
('bat36','boat3',6),
('bat37','boat3',7),
('bat38','boat3',8)
;

INSERT INTO Goboat.Boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat41','boat4',1),
('bat42','boat4',2),
('bat43','boat4',3),
('bat44','boat4',4),
('bat45','boat4',5),
('bat46','boat4',6),
('bat47','boat4',7),
('bat48','boat4',8)
;

INSERT INTO Goboat.Boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat51','boat5',1),
('bat52','boat5',2),
('bat53','boat5',3),
('bat54','boat5',4),
('bat55','boat5',5),
('bat56','boat5',6),
('bat57','boat5',7),
('bat58','boat5',8)
;
