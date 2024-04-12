-- version 1.0
-- Writen by: Frederik B. B. Jepsen
-- created: 12-04-2024
-- last modified:
-- Last Modified by:


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
('bat38','2024-04-07','lit_m1')
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

INSERT INTO Goboat.boats_batteries (Battery_ID,Boat_ID,Slot_number)
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

INSERT INTO Goboat.boats_batteries (Battery_ID,Boat_ID,Slot_number)
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

INSERT INTO Goboat.boats_batteries (Battery_ID,Boat_ID,Slot_number)
VALUES
('bat31','boat3',1),
('bat32','boat3',2),
('bat33','boat3',3),
('bat34','boat3',4)
;


