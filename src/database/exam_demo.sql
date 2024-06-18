-- Join the information from Data_boat and voltage table

-- One of the issues with this model is, that it is not certain, that we can ensure, that the Data_ID used to relate the data from Data_Boat and the voltage tables  

SELECT * FROM goboatv2.boat_log
INNER JOIN battery_log ON goboatv2.boat_log.data_ID=goboatv2.battery_log.data_ID
-- WHERE (boat_log.boat_ID='boat1' AND boat_log.data_ID='1');
WHERE boat_log.data_time > '2024-06-18 00:00:00'
ORDER BY boat_log.data_time ASC
