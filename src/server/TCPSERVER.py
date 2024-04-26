#Version 0.23 | Encoding UTF-8
#Created 23-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 26-04-2024



# I will try to make this a class, so it is a module.

# This does currently not crash, but it refuses a connection with anything.

import socket
import selectors
from xml_parser import XmlParser
import sql_insert_data as sql
import threading

"""
This needs to be event based with a que system, in order to ensure that all data gets into the database
"""

class SQL_socket:
    """
    SQL_socket(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024)

    This socket is used to recieve xml-files that are to be inserted into the SQL-server.

    
    """

    def __init__(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None) -> None:
        self.HOST=  HOST          # Symbolic name meaning all available interfaces
        self.PORT = PORT         # Arbitrary non-privileged port
        self.CONN_COUNTER = CONN_COUNTER    # Counter for connections
        self.BUFFER_SIZE = BUFFER_SIZE  # Receive Buffer size (power of 2)
        self.sel = selectors.DefaultSelector()
        self.user = user
        self.password = password
        self.host = host


        #Creates sockets
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)

        #This start the the listening process

     

    def accept(self,sock, mask):
        self.conn, self.addr = self.sock.accept() # Should be ready
        print('accepted', self.conn, 'from', self.addr)
        self.conn.setblocking(False)
        self.sel.register(self.conn, selectors.EVENT_READ, self.read)


    def read(self,sock, mask):

        data = b''
        while b"EOF" not in data: # runs while EOF(end of file) is not in the data, which is recieved last from the client. 
            try:
                data += self.conn.recv(self.BUFFER_SIZE) # used try except to avoid blocking error
            except BlockingIOError:
                continue
        
        self.sel.unregister(self.conn)
        self.conn.close()

        # Creates a XML-file out of the data string.
        xml_file= str(data[:-3], 'UTF-8')


        self.insert_data(xml_file)

        # Threading i not yet implemented

        #event = threading.Event(target=self.insert_data, args=(str(xml_file),),name=f'Insert_xml_thread_{self.CONN_COUNTER}')
       # event.set()
        self.CONN_COUNTER +=1




    def insert_data(self,xml):
        
        xml_parser= XmlParser(xsd_path="sch_status_data.xsd", xml_path=str(xml)) #inserets the xml data into the xml_parser from the client. 
        xml_parser.get_all_data()
        Goboat = sql.DatabaseConnection(user=self.user,password=self.password,host=self.host) # establish connection to the database
        input = xml_parser

        Goboat.insert_boat_data(boat_ID=input.boat_id,Date=input.date,Lok_lat=input.lok_lat,Lok_long=input.lok_long,Battery_temperatures=input.temp_list,Watt_hour=input.watt_hour,Voltage_array=input.voltage_list)





if __name__ == "__main__":
    test = SQL_socket(user="frederik",password="password")
    print('* TCP Server listening for incoming connections in port {}'.format(test.PORT))
    while True:
        events = test.sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
