#Version 0.10 | Encoding UTF-8
#Created by: Ib Leminen Mohr Nielsen
#Date: 04-04-2024    
# boot.py -- run on boot-up
from socket import *
import network 
"""
MicroPython code for ESP32.
Connects to WifI and sends a simple message.
"""

def connect_to_wifi(): 
    """
    Makes the ESP32 connect to WiFi.\n
    \n
    ------------
    PARAMETERS\n
    \n
    None:\n
    ------------
    RETURNS\n
    \n
    Returns "None"\n
    Return type is None.\n
    """
    ssid = "Linksys00339" #Network's name.
    key="GoBoat33" #Network's passcode.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected(): #Checks if ESP32 is connected to WiFi.
        wlan.connect(ssid, key) #Connects to WiFi if not connected. 
        while not wlan.isconnected(): #Pases loop if WiFi connection is established.
            pass

def client_to_server():
    """
    Connects the client to the server using TCP (socket), Make sure to be on same network as server and not eduroam.\n
    \n
    ------------
    PARAMETERS\n
    \n
    None:\n
    ------------
    RETURNS\n
    \n
    Returns "None"\n
    Return type is None.\n
    """
    
    server_ip = "192.168.1.140" #The server's IP adress, Raspberry Pi IP_Adress = 192.168.1.10
    server_port = 8888 
    buffer_size = 1024 
    message="Hello Group" #The message that gets sent to the server.
    payload=message
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((server_ip, server_port)) #Establishes connection to server.
    sock.send(bytes(payload,'utf-8')) #Sends the payload in bytes formatted in utf-8


#running the functions.
connect_to_wifi()
client_to_server()
