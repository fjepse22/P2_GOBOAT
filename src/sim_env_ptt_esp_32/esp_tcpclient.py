# Version 1.01 | Encoding UFT-8
# Created: 04-04-2024
# Created by: Ib Leminen Mohr Nielsen
# Modified by: Ib Leminen Mohr Nielsen
# Last Modified: 15-05-2024

import network 
import json
from socket import *

"""
MicroPython code for ESP32.
Connects to WifI and sends a simple message.
"""
class Client:
    def __init__(self, unit_dict, voltage_dict, temp_dict):
        """
        Initialises the class\n
        \n
        ------------
        PARAMETERS\n
        unit_dict: Dictionary for storing unit data\n
        voltage_dict: Dictionary for storing battery voltage data\n
        temp_dict: Dictionary for storing battery temperture data\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """
        self.unit_dict=unit_dict
        self.voltage_dict=voltage_dict
        self.temp_dict=temp_dict
        
    
    def _connect_to_wifi(self): #forbindelse til WiFi.
        """
        Makes it possible to connect to wifi\n
        \n
        ------------
        PARAMETERS\n
        Takes None\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        ssid = "Linksys00339" #Network's name.
        key="GoBoat33" #Network's passcode.
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected(): #Checks if ESP32 is connected to WiFi.
            wlan.connect(ssid, key) #Connects to WiFi if not connected. 
            while not wlan.isconnected(): #Pases loop if WiFi connection is established.
                pass

    def payload(self):
        """
        Method creates a payload for the message to be sent\n
        \n
        ------------
        PARAMETERS\n
        Takes None\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """
        byte_unit_dict=json.dumps(self.unit_dict).encode('utf-8')+b'#'
        byte_voltage_dict=json.dumps(self.voltage_dict).encode('utf-8')+b'#'
        byte_temp_dict=json.dumps(self.temp_dict).encode('utf-8')+b'#'
        message = byte_unit_dict+byte_voltage_dict+byte_temp_dict
        self.send_data(message)
    
    def send_data(self, message, SERVER_IP="192.168.1.10", SERVER_PORT=8888):
        """
        Connects the client to the server using TCP (socket)\n
        Raspberry Pi IP_Adress = 192.168.1.10\n
        Make sure to be on same network as server and not eduroam\n
        \n
        ------------
        PARAMETERS\n
        Takes None\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """
        
        self._connect_to_wifi()

        s = socket(AF_INET,SOCK_STREAM)

        try:
            s.connect((SERVER_IP, SERVER_PORT))
        except: 
            print("the connection coudn't be established")
            pass    

        try:
            header=len(message)
            s.send(header.to_bytes(3, 'big'))
            s.send(message)

        except OverflowError:
            print(f"{OverflowError}, the message is too long")
            
        except:
            print("the connection is broken")
        
        s.close()

      
