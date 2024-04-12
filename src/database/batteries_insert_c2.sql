-- testing creating a boat with batteries



-- dummy battery model
INSERT INTO Goboat.Battey_models (Battey_model_ID,Model_name,Max_voltage,Voltage_schema,Battery_type)
VALUES ('lit_m1','litiumion model 1','12','volt_skema','LitiumIon');


-- Dummy batteriries
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


