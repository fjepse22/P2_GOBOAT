# See https://mariadb-corporation.github.io/mariadb-connector-python/usage.html for documentation about the mariadb module.
# Version 1.26
# Writen by Frederik B. B. Jepsen
# Created 13-04-2024
# last modified: 14-05-2024
# modified by: Frederik Jepsen

# TESTER PULL REQUEST

import mariadb
from  logger import log
import xml_parser as xml_p

class DatabaseConnection:
    """
    The class ThreadManager is used to run the TCPSERVER on a thread.\n 

    List of class methods:\n
    - __init__(self,user,password,host,port=3306,database='Goboat', directory='',log_level = logging.ERROR): Initializes the class with the user, password, host, port, database, directory. and logging level\n
    - insert_boat_data(self,boat_ID,date,lok_lat,lok_long,temperature,watt,voltage_array): Inserts the data into the Goboat database.\n

    """
  
    def __init__(self,user,password,host,port=3306,database='Goboat', directory='',log_level = None):
       # self.logger = logging.getLogger(__name__) # This is used to log the errors that might occur.
       # self.logging=logging.basicConfig(filename=(directory+'/sql_insert.log'), format='%(asctime)s, %(levelname)s, %(message)s', encoding='utf-8', level=log_level) #This is used to format the log, and what information it should contain.


        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def insert_boat_data(self,boat_ID,date,lok_lat,lok_long,temperatures,watt,voltage_array):
        """
        This method connects to the Goboat database and insert the data recieved from the xml data.\n
        It will only insert the data, if the amount of batteries for the boat corresponding to the length of the voltage_array.\n
        It will insert data into the tables boat_log and Voltage.\n
        If somethings goes wrong no changes will be commited into the database.\n
        \n
        ------------
        PARAMETERS\n
        boat_ID: The ID of the boat\n
        date: The date and time of the data\n
        lok_lat: The latitude of the boat\n
        lok_long: The longitude of the boat\n
        temperatures: The temperature of the batteries in a list\n
        watt: The amount of watt hours\n
        voltage_array: The voltage of the batteries in a list\n
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
            log.debug(f'Connected sucessfully to {self.database} with user {self.user}')
        except mariadb.Error as e:
            log.error(f'Error connecting to MariaDB Platform: {e}')
        # Get Cursor
        cursor = connection.cursor()


        # The command to insert all data of the boat except the voltage of the battery.
        insert_data = f"""INSERT INTO goboatv2.boat_log (boat_ID,data_time,lok_lat,lok_long,watt)
        VALUES ('{boat_ID}','{date}','{lok_lat}','{lok_long}',{watt});"""
        

        # this command is used to find the Data_ID in order to link the data about battery voltage to the rest of the boat data.
        # it is possible to extract this information before you commit the data, as the Data_ID get reserved for the duration.
        find_Data_ID = f"""SELECT Data_ID
        From goboatv2.boat_log
        WHERE (boat_ID='{boat_ID}') AND (data_time='{date}'); """


        find_batteries =f""" SELECT bat_ID,slot_no
        FROM goboatv2.boat_conf
        WHERE (boat_ID='{boat_ID}');"""
        

        # fetch the batteri_id for each batteri in the boat.
        # it returns a list of tubles which is a surprise tool that we will use at later.
        try:
            cursor.execute(find_batteries)
            fetch = cursor.fetchall()
            batteries = fetch
        except mariadb.Error as e:
            log.error(f'Could not find batteries for the boat with ID {boat_ID}: {e}')
            cursor.close()
            connection.close()
            return
        

        # this check that the amount of batteries on the boat correnspont to the voltage_array data
        # if that is not the case, no data will be inserted into the Goboat database.
        if len(batteries) == len(voltage_array):
            pass    
        else:
            # raise Exception(f'The number of batteries on boat {boat_ID} in the database does not correspond to the amount of batteries comming from the xml-file')
            log.error(f'The number of batteries on boat {boat_ID} in the database does not correspond to the amount of batteries comming from the xml-file')
            cursor.close()
            connection.close()
            return

        try:
            cursor.execute(insert_data)
                
        except mariadb.Error as e:
            log.error(f"insert into table boat_log failed: {e}" )
            cursor.close()
            connection.close()
            return

        try:
            cursor.execute(find_Data_ID)
            fetch = cursor.fetchall()
            Data_ID = fetch[0][0]
        except mariadb.Error as e:
            log.error(f'select statement failed could not find Data_ID {Data_ID} in table boat_log {e}')
            cursor.close()
            connection.close()
            return


        # This logic insert the data about voltage for each battery
        # unforfunally it does not work to write the sql statement as a variable and call that varible in the cursor.execute command.
        # Therefore this string is copied to the cursor.execute() command

        try:
            for i in range(0,len(voltage_array)):
                cursor.execute(f""" INSERT INTO goboatv2.battery_log (Data_ID,bat_ID,temperature,voltage)
            VALUES ('{Data_ID}','{batteries[i][0]}','{temperatures[i]}','{voltage_array[i]}');""")
                
        # Shows the dublicate entry as boat_ID compined with time.
        except mariadb.IntegrityError as e:
            log.error(f"failed to insert data to the voltage table {e} with the boat_ID: {boat_ID} and time {date}")
            cursor.close()
            connection.close()
        except mariadb.Error as e:
            log.error(f"failed to insert data to the voltage table {e}")
            cursor.close()
            connection.close()
            return


        # if everything went without errors, the updated values are implementet
        connection.commit()
        # free resources
        cursor.close()
        connection.close()
        log.info(f'Data from xml-file inserted to database with Data_ID: {Data_ID}, Boat_ID: {boat_ID} log_time: {date}')

if __name__ == '__main__':

    ud= {"id" : 2, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : "14:12:11", "p_draw" : 0}
    vd = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    td = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

    # Testserver on Frederik's own computer.
    Goboat = DatabaseConnection(user="frederik",password="password",host="127.0.0.1",database='goboatv2',directory="C:/Users/frede/Downloads")
    data = xml_p.XmlParser(directory="C:/Users/frede/Downloads", unit_dict=ud, voltage_dict=vd, temp_dict=td)
    data.get_all_data()

    Goboat.insert_boat_data(boat_ID=data.boat_id,date=data.date,lok_lat=data.lok_lat,lok_long=data.lok_long,temperatures=data.temp_list,watt=data.watt,voltage_array=data.voltage_list)

