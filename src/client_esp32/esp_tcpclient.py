# Version 1.00 | Encoding UFT-8
# Created: 04-04-2024
# Created by: Ib Leminen Mohr Nielsen
# Modified by: Ib Leminen Mohr Nielsen
# Last Modified: 10-05-2024

from socket import *
import network 
import json

"""
MicroPython code for ESP32.
Connects to WifI and sends a simple message.
"""
class Client:
    def __init__(self):
        pass
    
    def _connect_to_wifi(self): #forbindelse til WiFi.
        """
        Method makes it possible to connect ESP32 to WiFi.
        """

        ssid = "Linksys00339" #Network's name.
        key="GoBoat33" #Network's passcode.
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected(): #Checks if ESP32 is connected to WiFi.
            wlan.connect(ssid, key) #Connects to WiFi if not connected. 
            while not wlan.isconnected(): #Pases loop if WiFi connection is established.
                pass

    def send_data(self, unit_dict, voltage_dict, temp_dict, SERVER_IP="192.168.1.10", SERVER_PORT=8888):
        """
        Connects the client to the server using TCP (socket)
        Raspberry Pi IP_Adress = 192.168.1.10
        Make sure to be on same network as server and not eduroam
        """
        self._connect_to_wifi()

        buffer_size = 1024 
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT)) #Establishes connection to server.

        s.send(json.dumps(unit_dict).encode('utf-8')+b'#')
        s.send(json.dumps(voltage_dict).encode('utf-8')+b'#')
        s.send(json.dumps(temp_dict).encode('utf-8')+b'#')
        s.send(b'EOF')
