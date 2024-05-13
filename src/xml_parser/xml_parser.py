#Version 1.01 | Encoding UTF-8
#Created 13-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 13-05-2024

import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from packet_controller import validate
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

    def __init__(self,xsd_path="sch_status_data.xsd", directory="", unit_dict={},voltage_dict={},temp_dict={},xml_path=None):
        self.logger = logging.getLogger(__name__)
        self.logging=logging.basicConfig(filename=(directory+'/error.log'), format='%(asctime)s, %(levelname)s, %(message)s', encoding='utf-8', level=logging.DEBUG)
        self.voltage_list = []  #Voltage from each battery.
        self.temp_list = []  #Temperature of each battery.
        self.watt = float(0) #Based on Draw from xml.
        self.lok_lat =float(0)  #Latitude used to locate the boat.
        self.lok_long = float(0)  #Longitude used to locate the boat. 
        self.date = str("")  #yyyy-mm-dd hh:mm:ss format 
        self.boat_id = str("")  #Uniqe ID for each boat.
        self.read_xml((xsd_path),unit_dict, voltage_dict, temp_dict, xml_path) #Reads the XML file and stores it in self.root
        
    def read_xml(self,xsd_path,unit_dict, voltage_dict, temp_dict, xml_path=None):
        """
        If dictionary it will try to create XML first and afterwards reads the XML file and stores it in self.root\n
        There is three ways to input data, in dictionaries, the path to a XML document or a XML string\n
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
        Returns "None"\n
        Return None\n
        """
        self.valid_xml=True
        if type(xml_path)!=type(""):
            try:
                create_xml=CreateXML(unit_dict, voltage_dict, temp_dict)
                xml_path=create_xml.generateXML()
            except:
                self.logger.error(f"""File: generate_xml.py\nErrorType: CreateXML\nThe dictionary is not formatted right\n""")
                self.valid_xml=False
        
        if self.valid_xml==True:
            try:
                try:
                    self.root = ET.fromstring(open(xml_path).read()) #Reads the XML file and stores it in root.
                except:
                    self.root = ET.fromstring(xml_path) #Reads the XML data and stores it in root.
            except ET.ParseError:
                self.logger.error(f"""File: xml_parser.py\nErrorType: ET.ParseError\nThe string is not in XML format\n""")
                self.valid_xml=False

            if self.valid_xml==True and not validate(xsd_path,xml_path):
                self.logger.error(f"""File: packet_controller.py\nThe XML file is not valid according to the XSD schema\n""")
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
        Voltage for battery {self.voltage_list}
        Temperature for battery {self.temp_list}
        Boat ID = {self.boat_id}
        Lattitude = {self.lok_lat}
        Longitude = {self.lok_long}
        Event time = {self.date}
        Watt = {self.watt}
        """)

if __name__ == '__main__':
    ud= {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : "14:12:10", "p_draw" : 0}
    vd = {"batt_1" : 12, "batt_2" : 12, "batt_3" : 12, "batt_4": 13, "batt_5": 15, "batt_6": 12, "batt_7" : 11, "batt_8" : 9}
    td = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

    xml_parser= XmlParser(directory="/Users/ibleminen/Downloads/test/rasp/", unit_dict=ud, voltage_dict=vd, temp_dict=td, xml_path=None) #if you want to change directory, you can add it as a parameter here ex. for macOS XmlParser(directory="/Users/ibleminen/Downloads/test/rasp") 
    xml_parser.get_all_data()
    print(xml_parser)
