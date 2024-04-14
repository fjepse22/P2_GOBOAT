#Version 0.10 | Encoding UTF-8
#Created 13-04-2024
#Created by: Ib Leminen Mohr Nielsen
# Last modified by: Frederik B. B. Jepsen
# Last modified 13-04-2024

import xml.etree.ElementTree as ET
from datetime import datetime
class XmlParser:
    """
    The class XmlParser is used to read an XML file and extract data from it. The data is stored in the class variables.\n 

    List of class methods:\n
    - get_voltage(): Looks for every battery in the xml-file and reads the voltage from it, and appends it to self.voltage_list\n

    - get_time(): b: Looks for time sent from the xml file and adds the current date to it.\n

    - get_std_data(): Looks for the rest of the more simple data and adds it to variables\n

    - get_all_data(): call the methods get_voltage(), get_time() and get_std_data()
    """

    def __init__(self):
        self.root = ET.fromstring(open('status_data_8batt.xml').read()) #Reads the XML file and stores it in root.
        self.voltage_list = []    #Based on Draw from xml.
        self.boat_id = str("")  #Uniqe ID for each boat.
        self.lok_lat = int(0)  #Latitude used to locate the boat.
        self.lok_long = int(0)  #Longitude used to locate the boat. 
        self.date = str("")  #yyyy-mm-dd hh:mm:ss format 
        self.watt_hour = int(0)    #Watt hour used for power draw.


    def __str__(self) -> str:
        return(f"""
        Voltage for battery {self.voltage_list}
        Boat ID = {self.boat_id}
        Lattitude = {self.lok_lat}
        Longitude = {self.lok_long}
        Event time = {self.date}
        What hour = {self.watt_hour}
        """)


    def get_voltage(self):
        """
        Looks for every battery in the xml-file and reads the voltage from it, and appends it to self.voltage_list\n
        \n
        ------------
        PARAMETERS\n
        \n
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "self.voltage_list"\n
        Return type is list. List element type is FLOAT\n
        """
      
        i=0
        while True:
            Battery_number=(".//Battery"+str(i+1))  #Increment Battery number to get the right name/root.

            if self.root.find(Battery_number+"/Voltage") == None:  #Looks to see if there is another battery, if None it doesnt exist.
                break

            for data in self.root.findall(Battery_number):  #Looks for specific battery in xml file, for instance Battery1
                self.voltage_list.append(data.find(".//Voltage").text) #appends the value of voltage to self.voltage_list.
                i+=1  
                
        return self.voltage_list
    
    
    def get_time(self):
        """
        Looks for time sent from the xml file and adds the current date to it.\n
        \n
        ------------
        PARAMETERS\n
        \n
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "self.date"\n
        Return type is string. The string is in yyyy-mm-dd hh:mm:ss format ex. 2024-04-11 14:02:46\n
        """
      
        local_time=datetime.today().strftime("%Y-%m-%d")  #For getting year, month and day 
        time = self.root.find(".//boatData/Time").text  #Finds time from XML file, time is hr, min and sec
        self.date=local_time+" "+time  

        return self.date

    def get_std_data(self):
        """
        Looks for the rest of the more simple data and adds it to variables.\n
        \n
        ------------
        PARAMETERS\n
        \n
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "self.watt_hour"\n
        Return type is string. The string is the value of Draw in the XML file.\n

        Returns "self.boat_id"\n
        Return type is string. The string is the ID of the boat.\n

        Returns "self.lok_lat"\n
        Return type is string. The string is the latitude of the boat.\n

        Returns "self.lok_long"\n
        Return type is string. The string is the longitude of the boat.\n
        """
        self.watt_hour = self.root.find(".//battData/Draw").text  #Looks for Draw in XML file, which is the value of watt hour.
        self.boat_id = "boat"+self.root.find(".//boatData/ID").text  #Looks for ID number in XML and adds "boat" to it.
        self.lok_lat = self.root.find(".//boatData/PositionLat").text  #Looks for PositionLat in XML file.
        self.lok_long = self.root.find(".//boatData/PositionLon").text  #Looks for PositionLon in XML file.

        return self.watt_hour, self.boat_id, self.lok_lat, self.lok_long
    
    def get_all_data(self):
        """
        get_all_data(self)

        This method call get_voltage(),get_time() and get_std_data()
        This ensures all the data from the xml-file is extracted by one method call.

        """


        self.get_voltage()
        self.get_time()
        self.get_std_data()
        



if __name__ == '__main__':
    xml_parser= XmlParser()
   # xml_parser.get_voltage()
   # xml_parser.get_time()
   # xml_parser.get_std_data()
    xml_parser.get_all_data()

    print(xml_parser)
