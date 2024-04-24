#Version 0.22 | Encoding UTF-8
#Created 23-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 24-04-2024

import socket
import selectors
from xml_parser import XmlParser
import sql_insert_data as sql

"""
This needs to be event based with a que system, in order to ensure that all data gets into the database
"""

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 1024  # Receive Buffer size (power of 2)
sel = selectors.DefaultSelector()

print('* TCP Server listening for incoming connections in port {}'.format(PORT))

def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    #print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = b''
    while b"EOF" not in data: # runs while EOF(end of file) is not in the data, which is recieved last from the client. 
        try:
            data += conn.recv(BUFFER_SIZE) # used try except to avoid blocking error
        except BlockingIOError:
            continue
    
    sel.unregister(conn)
    conn.close()

    xml_parser= XmlParser(xsd_path="sch_status_data.xsd", xml_path=str(data[:-3], 'UTF-8')) #inserets the xml data into the xml_parser from the client. 
    xml_parser.get_all_data()
    Goboat = sql.DatabaseConnection(user="testuser",password="testpassword",host="127.0.0.1") # establish connection to the database
    input = xml_parser

    Goboat.insert_boat_data(boat_ID=input.boat_id,Date=input.date,Lok_lat=input.lok_lat,Lok_long=input.lok_long,Battery_temperatures=input.temp_list,Watt_hour=input.watt_hour,Voltage_array=input.voltage_list)
    #inserts the data into the database

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
