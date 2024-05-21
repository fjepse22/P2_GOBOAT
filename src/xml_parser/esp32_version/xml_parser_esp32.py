#Version 1.10 | Encoding UTF-8
#Created 13-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 21-05-2024

import xml.etree.ElementTree as ET
import json
from logger import log
from datetime import datetime
from packet_controller_esp32 import PacketController
from generate_xml import CreateXML

class XmlParser:
    """
    The class XmlParser is used to read an XML file and extract data from it. The data is stored in the class variables.\n 

    List of class methods:\n
    - get_voltage(): Looks for every battery in the xml-file and reads the voltage from it, and appends it to self.voltage_list\n

    - get_time(): b: Looks for time sent from the xml file and adds the current date to it.\n

    - get_std_data(): Looks for the rest of the more simple data and adds it to variables\n

    - __str__(): Gathers the data in a string, making it nice to read, if printed \n

    """

    def __init__(self,xsd_path="sch_status_data.xsd", directory="", data=None):
        self.voltage_list = []  #Voltage from each battery.
        self.temp_list = []  #Temperature of each battery.
        self.watt = float(0) #Based on Draw from xml.
        self.lok_lat =float(0)  #Latitude used to locate the boat.
        self.lok_long = float(0)  #Longitude used to locate the boat. 
        self.date = str("")  #yyyy-mm-dd hh:mm:ss format 
        self.boat_id = str("")  #Uniqe ID for each boat.
        self.read_xml((xsd_path),data) #Reads the XML file and stores it in self.root
        
    def read_xml(self,xsd_path, data):
        """
        The method read_xml is used to read the dictionaries and create xml from them and afterwards store it in self.root. If the XML file is not valid, it will not store it in self.root.\n
        \n
        ------------
        PARAMETERS\n
        xds_path = The path of the file to check xml-integrety.\n
        xml_input = xml in string format\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """
        self.valid_xml=True

        try:
            xml_input=CreateXML().bytes_to_xml(data)
            self.root = ET.fromstring(xml_input) #Reads the XML data and stores it in root.
        except:
            log.error(f"""File: generate_xml.py: The input is not formatted right and XML cannot be created""")
            self.valid_xml=False


        if self.valid_xml==True and not PacketController().validate(xsd_path, xml_input):
            log.error(f"""File: packet_controller.py: The XML file is not valid according to the XSD schema""")
            self.valid_xml=False
            
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

        Returns "None"\n
        Return None\n
        """
        
        i=0
        while True:
            Battery_number=(".//Battery"+str(i+1))  #Increment Battery number to get the right name/root.

            if self.root.find(Battery_number+"/Voltage") == None:  #Looks to see if there is another battery, if None it doesnt exist.
                break

            for data in self.root.findall(Battery_number):  #Looks for specific battery in xml file, for instance Battery1
                self.voltage_list.append(data.find(".//Voltage").text) #Appends the value of voltage to self.voltage_list.
                self.temp_list.append(data.find(".//Temperature").text ) #Appends the value of temperature in celsius to self.temp_list.
                i+=1  
    
    
    def get_time(self):
        """
        Looks for time sent from the xml file and adds the current date to it. In the format yyyy-mm-dd hh:mm:ss format ex. 2024-04-11 14:02:46\\n
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
        local_time=datetime.today().strftime("%Y-%m-%d")  #For getting year, month and day 
        time = self.root.find(".//boatData/Time").text  #Finds time from XML file, time is hr, min and sec
        self.date=local_time+" "+time  

    def get_std_data(self):
        """
        Looks for the rest of the more simple data and if self.valid_xml is True it adds it to variables. If False it will not try to read the data.\n
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
        self.watt = self.root.find(".//battData/Draw").text  #Looks for Draw in XML file, which is the value of watt.
        self.boat_id = "boat"+self.root.find(".//boatData/ID").text  #Looks for ID number in XML and adds "boat" to it.
        self.lok_lat = self.root.find(".//boatData/PositionLat").text  #Looks for PositionLat in XML file.
        self.lok_long = self.root.find(".//boatData/PositionLon").text  #Looks for PositionLon in XML file.
    
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
        if self.valid_xml==True:
            self.get_volt_temp()
            self.get_time()
            self.get_std_data()
    
    def __str__(self) -> str:
        """
        Gathers the data in a string, making it nice to read, if printed.\n
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
        return(f"""
        Valid XML = {self.valid_xml}
        Voltage for battery {self.voltage_list}
        Temperature for battery {self.temp_list}
        Boat ID = {self.boat_id}
        Lattitude = {self.lok_lat}
        Longitude = {self.lok_long}
        Event time = {self.date}
        Watt = {self.watt}
        """)

if __name__ == '__main__':
    local_time=datetime.today().strftime("%H:%M:%S")
    unit_dict = {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : local_time, "p_draw" : 1}
    voltage_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    temp_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    
    # converts the dictionaries to bytes and encodes it to utf-8, and adds a '#' to the end of the string.
    bud=json.dumps(unit_dict).encode('utf-8')+b'#'
    bvd=json.dumps(voltage_dict).encode('utf-8')+b'#'
    btd=json.dumps(temp_dict).encode('utf-8')+b'#'
    valid_byte_dict = bud+bvd+btd

    xml_parser= XmlParser(directory="/Users/ibleminen/Downloads/test/ESP32_VERSION/Server ESP32", data=valid_byte_dict) #if you want to change directory, you can add it as a parameter here ex. for macOS XmlParser(directory="/Users/ibleminen/Downloads/test/rasp") 
    xml_parser.get_all_data()
    
    print(xml_parser)
