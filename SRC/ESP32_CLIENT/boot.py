# boot.py -- run on boot-up
from socket import *
"""
MicroPython code for ESP32.
Connects to WifI and sends a simple message.
"""

def connect_to_wifi(): #forbindelse til WiFi.
"""
Function makes it possible to connect ESP32 to WiFi.
"""
    import network 
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
Connects the client to the server using TCP (socket)
Raspberry Pi IP_Adress = 192.168.1.10
Make sure to be on same network as server and not eduroam
"""
    server_ip = "192.168.1.140" #The server's IP adress 
    server_port = 8888 
    buffer_size = 1024 
    message="Hello Group" #The message that gets sent to the server.
    payload=message
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((server_ip, server_port)) #Establishes connection to server.
    sock.send(bytes(payload,'utf-8')) #Sends the payload in bytes formatted in utd-8

#running the functions.
connect_to_server()
client_to_server()
