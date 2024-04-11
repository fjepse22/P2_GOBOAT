import xml.etree.ElementTree as ET
from datetime import datetime
import numpy as np
"""
This code is made for parsing XML files from ESP32 devices on GoBoat.
"""

class xml_parser:
    def __init__(self):
        self.root = ET.fromstring(open('status_data_8batt.xml').read()) 
        self.nr_of_batt = int(0)  #Number of batteries
        self.Voltage_Array = np.zeros(100)  #Array for storing voltage values from each battery. 
        self.Amperage = int(0)  #Based on Draw from xml.
        self.Boat_ID = str("")  #Uniqe ID for each boat.
        self.lok_lat = int(0)  #Latitude used to locate the boat.
        self.lok_long = int(0)  #Longitude used to locate the boat. 
        self.date = str("")  #yyyy-mm-dd hh:mm:ss format 

    def get_voltage(self):
        """
        Finds the battery tags in the XML file and reads the voltage for each battery. The voltages are stored in self.Voltage_Array

        Returns Array with voltages and number of batteries.
        """
      
        i=0
        while True:
            Battery_number=(".//Battery"+str(i+1))  #Increment Battery number to get the right name/root.
            for data in self.root.findall(Battery_number):  #Looks for specific battery in xml file, for instance Battery1
                self.Voltage_Array[i] = data.find(".//Voltage").text #Writes the voltage into the array in the index of i
                i+=1  

            if self.root.find(Battery_number+"/Voltage") == None:  #Looks to see if there is another battery, if None it doesnt exist.
                self.Voltage_Array=self.Voltage_Array[0:i]  #Makes the list, shorter to match the number of batteries.
                self.nr_of_batt = i  
                break

        return self.Voltage_Array, self.nr_of_batt
    
    def get_time(self):
        """
        Adds the year, month and day to the time from the XML file.

        Returns the time in yyyy-mm-dd hh:mm:ss format ex. 2024-04-11 14:02:46
        """
      
        local_time=datetime.today().strftime("%Y-%m-%d")  #For getting year, month and day 
        Time = self.root.find(".//boatData/Time").text  #Finds time from XML file, time is hr, min and sec
        self.date=local_time+" "+Time  

        return self.date

    def get_std_data(self):
        """
        Looks for the rest of the more simple data. 

        Returns Amperage, Boat_ID, lok_lat and lok_long.
        """
        self.Amperage = self.root.find(".//battData/Draw").text  #Looks for Draw in XML file.
        self.Boat_ID = "boat"+self.root.find(".//boatData/ID").text  #Looks for ID number in XML and adds "boat" to it.
        self.lok_lat = self.root.find(".//boatData/PositionLat").text  #Looks for PositionLat in XML file.
        self.lok_long = self.root.find(".//boatData/PositionLon").text  #Looks for PositionLon in XML file.

        return self.Amperage, self.Boat_ID, self.lok_lat, self.lok_long
        
xml_parser=xml_parser()
xml_parser.get_voltage()
xml_parser.get_time()
xml_parser.get_std_data()
