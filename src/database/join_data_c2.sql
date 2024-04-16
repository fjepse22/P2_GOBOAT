-- Join the information from Data_boat and voltage table

-- One of the issues with this model is, that it is not certain, that we can ensure, that the Data_ID used to relate the data from Data_Boat and the voltage tables  

USE Goboat;

SELECT * FROM Goboat.Data_boat
INNER JOIN Voltage ON Goboat.data_boat.Data_ID=Goboat.voltage.Data_ID
WHERE (data_boat.Boat_ID='boat2' AND data_boat.Data_ID='10');