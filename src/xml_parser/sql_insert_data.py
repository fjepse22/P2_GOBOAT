# See https://mariadb-corporation.github.io/mariadb-connector-python/usage.html for documentation about the mariadb module.
# Version 1.21
# Writen by Frederik B. B. Jepsen
# Created 13-04-2024
# last modified: 1-05-2024
# modified by: Frederik Jepsen, Ib Leminen

# TESTER PULL REQUEST

import mariadb
import logging
import xml_parser as xml_p

class DatabaseConnection:
    """
    The class ThreadManager is used to run the TCPSERVER on a thread.\n 

    List of class methods:\n
    - __init__(self,user,password,host,port=3306,database='Goboat', directory=''): Initializes the class with the user, password, host, port, database and directory.\n
    - insert_boat_data(self,boat_ID,Date,Lok_lat,Lok_long,Battery_temperature,Watt_hour,Voltage_array): Inserts the data into the Goboat database.\n

    """
  
    def __init__(self,user,password,host,port=3306,database='Goboat', directory=''):
        self.logger = logging.getLogger(__name__) # This is used to log the errors that might occur.
        self.logging=logging.basicConfig(filename=(directory+'/sql_insert.log'), format='%(asctime)s, %(levelname)s, %(message)s', encoding='utf-8', level=logging.DEBUG) #This is used to format the log, and what information it should contain.


        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def insert_boat_data(self,boat_ID,Date,Lok_lat,Lok_long,Battery_temperatures,Watt_hour,Voltage_array):
        """
        This method connects to the Goboat database and insert the data recieved from the xml data.\n
        It will only insert the data, if the amount of batteries for the boat corresponding to the length of the Voltage_array.\n
        It will insert data into the tables Data_Boat and Voltage.\n
        If somethings goes wrong no changes will be commited into the database.\n
        \n
        ------------
        PARAMETERS\n
        boat_ID: The ID of the boat\n
        Date: The date and time of the data\n
        Lok_lat: The latitude of the boat\n
        Lok_long: The longitude of the boat\n
        Battery_temperatures: The temperature of the batteries in a list\n
        Watt_hour: The amount of watt hours\n
        Voltage_array: The voltage of the batteries in a list\n
        \n
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """

        try:
            connection = mariadb.connect(user = self.user, password = self.password,host = self.host,port = self.port, database = self.database)
            self.logger.info(f'Connected sucessfully to {self.database} with user {self.user}')
        except mariadb.Error as e:
            self.logger.error(f'Error connecting to MariaDB Platform: {e}')
        # Get Cursor
        cursor = connection.cursor()


        # The command to insert all data of the boat except the voltage of the battery.
        insert_data = f"""INSERT INTO Goboat.Data_Boat (Boat_ID,Data_time,Lok_lat,Lok_long,Watt_hour)
        VALUES ('{boat_ID}','{Date}','{Lok_lat}','{Lok_long}',{Watt_hour});"""
        

        # this command is used to find the Data_ID in order to link the data about battery voltage to the rest of the boat data.
        # it is possible to extract this information before you commit the data, as the Data_ID get reserved for the duration.
        find_Data_ID = f"""SELECT Data_ID
        From Goboat.Data_Boat
        WHERE (Boat_ID='{boat_ID}') AND (Data_time='{Date}'); """


        find_batteries =f""" SELECT Battery_ID,Slot_number
        FROM Goboat.Boats_batteries
        WHERE (Boat_ID='{boat_ID}');"""
        

        # fetch the batteri_id for each batteri in the boat.
        # it returns a list of tubles which is a surprise tool that we will use at later.
        try:
            cursor.execute(find_batteries)
            fetch = cursor.fetchall()
            batteries = fetch
        except mariadb.Error as e:
            self.logger.error(f'Could not find batteries for the boat with ID {boat_ID}: {e}')
            cursor.close()
            connection.close()
            return
        

        # this check that the amount of batteries on the boat correnspont to the voltage_array data
        # if that is not the case, no data will be inserted into the Goboat database.
        if len(batteries) == len(Voltage_array):
            pass    
        else:
            # raise Exception(f'The number of batteries on boat {boat_ID} in the database does not correspond to the amount of batteries comming from the xml-file')
            self.logger.error(f'The number of batteries on boat {boat_ID} in the database does not correspond to the amount of batteries comming from the xml-file')
            cursor.close()
            connection.close()
            return

        try:
            cursor.execute(insert_data)
                
        except mariadb.Error as e:
            self.logger.error(f"insert into table Data_boat failed: {e}" )
            cursor.close()
            connection.close()
            return

        try:
            cursor.execute(find_Data_ID)
            fetch = cursor.fetchall()
            Data_ID = fetch[0][0]
        except mariadb.Error as e:
            self.logger.error(f'select statement failed could not find Data_ID {Data_ID} in table Data_boat {e}')
            cursor.close()
            connection.close()
            return


        # This logic insert the data about voltage for each battery
        # unforfunally it does not work to write the sql statement as a variable and call that varible in the cursor.execute command.
        # Therefore this string is copied to the cursor.execute() command
        
        # Inserts the 
        try:
            for i in range(0,len(Voltage_array)):
                cursor.execute(f""" INSERT INTO Goboat.Voltage (Data_ID,Battery_ID,Battery_temperature,Battery_voltage)
            VALUES ('{Data_ID}','{batteries[i][0]}','{Battery_temperatures[i]}','{Voltage_array[i]}');""")
        except mariadb.Error as e:
            self.logger.error(f"failed to insert data to the voltage table {e}")
            cursor.close()
            connection.close()
            return


        # if everything went without errors, the updated values are implementet
        connection.commit()
        # free resources
        cursor.close()
        connection.close()
        self.logger.info(f'Data from xml-file inserted to database with Data_ID: {Data_ID}')

if __name__ == '__main__':

    # Testserver on Frederik's own computer.
    Goboat = DatabaseConnection(user="frederik",password="password",host="127.0.0.1")
    data = xml_p.XmlParser()
    data.get_all_data()

    Goboat.insert_boat_data(boat_ID=data.boat_id,Date=data.date,Lok_lat=data.lok_lat,Lok_long=data.lok_long,Battery_temperatures=data.temp_list,Watt_hour=data.watt_hour,Voltage_array=data.voltage_list)

