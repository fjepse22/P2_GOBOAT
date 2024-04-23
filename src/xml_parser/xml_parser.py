#Version 0.16 | Encoding UTF-8
#Created 13-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 23-04-2024

import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from lxml import etree
from packet_controller import validate

class XmlParser:
    """
    The class XmlParser is used to read an XML file and extract data from it. The data is stored in the class variables.\n 

    List of class methods:\n
    - get_voltage(): Looks for every battery in the xml-file and reads the voltage from it, and appends it to self.voltage_list\n

    - get_time(): b: Looks for time sent from the xml file and adds the current date to it.\n

    - get_std_data(): Looks for the rest of the more simple data and adds it to variables\n
    """

    def __init__(self,xsd_path="sch_status_data.xsd",xml_path="status_data.xml"):
        self.logger = logging.getLogger(__name__)
        self.logging=logging.basicConfig(filename='error.log', format='%(asctime)s, %(levelname)s, %(message)s', encoding='utf-8', level=logging.DEBUG)
        self.voltage_list = []  #Voltage from each battery.
        self.temp_list = []  #Temperature of each battery.
        self.watt_hour = int(0) #Based on Draw from xml.
        self.lok_lat = int(0)  #Latitude used to locate the boat.
        self.lok_long = int(0)  #Longitude used to locate the boat. 
        self.date = str("")  #yyyy-mm-dd hh:mm:ss format 
        self.boat_id = str("")  #Uniqe ID for each boat.
        self.read_xml(xsd_path,xml_path)
    
    def read_xml(self,xsd_path,xml_path):
        """
        Reads the XML file and stores it in self.root\n
        The XML-file can eithe be found via a file directory or recieved via xml\n
        This method should only called by the __init__ method
        \n
        ------------
        PARAMETERS\n
        xds_path = The path of the file to check xml-integrety.\n
        xml_path = The path to the xml-file or the string in xml-format"\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "self.root"\n
        Return type is ElementTree\n
        """
        
        try:
            try:
                self.root = ET.fromstring(open(xml_path).read()) #Reads the XML file and stores it in root.
            # if xml_path is not a path but a string, the program wil read the string as an xml-file.
            except:
                self.root = ET.fromstring(xml_path) #Reads the XML file and stores it in root.
        except FileNotFoundError:
            self.logger.error("File: status_data.xml"+"\n"+"      The file status_data.xml does not exist")
            exit(1)
        
        except ET.ParseError:
            self.logger.error("File: status_data.xml"+"\n"+"      The file is not valid XML")
            exit(1)

        if not validate(xsd_path,xml_path):
            self.logger.error("File: status_data.xml"+"\n"+"      The XML file is not valid according to the XSD schema")
            exit(1)

        
        return self.root
            
    def get_volt_temp(self):
        """
        Looks for every battery in the xml-file and reads the voltage and temperature from it, and appends it to self.voltage_list and self.temp_list\n
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

        Returns "self.temp_list"\n
        Return type is list. List element type is FLOAT\n
        """
        
        i=0
      ##  self.read_xml()
        while True:
            Battery_number=(".//Battery"+str(i+1))  #Increment Battery number to get the right name/root.

            if self.root.find(Battery_number+"/Voltage") == None:  #Looks to see if there is another battery, if None it doesnt exist.
                break

            for data in self.root.findall(Battery_number):  #Looks for specific battery in xml file, for instance Battery1
                self.voltage_list.append(data.find(".//Voltage").text) #Appends the value of voltage to self.voltage_list.
                self.temp_list.append(data.find(".//Temperature").text ) #Appends the value of temperature in celsius to self.temp_list.
                i+=1  
                
        return self.voltage_list, self.temp_list
    
    
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
       # self.read_xml()
        
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
      #  self.read_xml()

        self.watt_hour = self.root.find(".//battData/Draw").text  #Looks for Draw in XML file, which is the value of watt hour.
        self.boat_id = "boat"+self.root.find(".//boatData/ID").text  #Looks for ID number in XML and adds "boat" to it.
        self.lok_lat = self.root.find(".//boatData/PositionLat").text  #Looks for PositionLat in XML file.
        self.lok_long = self.root.find(".//boatData/PositionLon").text  #Looks for PositionLon in XML file.

        return self.watt_hour, self.boat_id, self.lok_lat, self.lok_long
    
    def get_all_data(self):
        """
        Collects all data from the xml-file in a single method.\n
        \n
        ------------
        PARAMETERS\n
        \n
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """

        self.get_volt_temp()
        self.get_time()
        self.get_std_data()
    
    def __str__(self) -> str:
        return(f"""
        Voltage for battery {self.voltage_list}
        Temperature for battery {self.temp_list}
        Boat ID = {self.boat_id}
        Lattitude = {self.lok_lat}
        Longitude = {self.lok_long}
        Event time = {self.date}
        Watt hour = {self.watt_hour}
        """)
    


if __name__ == '__main__':

    xml_parser= XmlParser()
    xml_parser.get_all_data()
    print(xml_parser)

