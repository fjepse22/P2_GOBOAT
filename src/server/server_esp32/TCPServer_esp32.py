#Version 1.02 | Encoding UTF-8
#Created 23-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 14-05-2024

import socket
import selectors
import json
import time
from logger import log
import sql_insert_data as sql
from xml_parser_esp32 import XmlParser

"""
This needs to be event based with a que system, in order to ensure that all data gets into the database
"""

class SQL_socket:
    """
    This socket is used to recieve xml-files that are to be inserted into the SQL-server.\n
    It can only connect to the Goboat database on port 3306.\n
    Once the object is made it will start to listen on. \n
    \n
    
    List of class methods:\n
    - __init__(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None): Initialises the object and starts the process to listen\n

    - __accept(self,sock, mask): Used to establish a connection to a client, that sends a xml-file.\n

    - __read(self, sock, mask): This method is used to recieve the xml-data from a client and insert it into the database\n

    - __insert_data(self,xml):  This method is used to connect to the Goboat database and insert the data from the xml-file, should only be called by the __read() method. \n

    - run(self): This method calls the loop that will constantly listen for something on the specified port self.PORT\n
    """

    def __init__(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None, directory="/home/Gruppe250/test",database='goboatv2') -> None:
        """
         Initialises the object and starts the process to listen
        """


        self.HOST=  HOST                        # Symbolic name meaning all available interfaces
        self.PORT = PORT                        # Arbitrary non-privileged port
        self.CONN_COUNTER = CONN_COUNTER        # Counter for connections
        self.BUFFER_SIZE = BUFFER_SIZE          # Receive Buffer size (power of 2)
        self.sel = selectors.DefaultSelector()  # Selector for the sockets, used for event based sockets
        self.user = user                        # Username to the database
        self.password = password                # Password to the database
        self.host = host                        # Where the database hosts the database
        self.directory = directory              # Directory to the folder
        self.database = database                # The name of the database

        #Creates sockets
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.__accept)
        
        #This start the the listening process

    def __accept(self,sock, mask):
        """
        This private method is used to establish a connection to a client, that sends a xml-file, Should not be run by a user.\n
        \n
        ------------
        PARAMETERS\n
        sock:\n
        mask:\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """

        self.conn, self.addr = self.sock.accept() # Should be ready
        self.conn.setblocking(False)
        self.sel.register(self.conn, selectors.EVENT_READ, self.__read)


    def __read(self,sock, mask): 
        """
        This private method is used to recieve the xml-data from a client and insert it into the SQL-database\n
        \n
        ------------
        PARAMETERS\n
        sock:\n
        mask:\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """
        
        data=b''
        header = self.conn.recv(3)
        log.debug(f"header length {int.from_bytes(header, 'big')}")
        
        start_time = time.time()
        while len(data) < int.from_bytes(header, 'big'):
            try:
                data += self.conn.recv(int.from_bytes(header, 'big'))
            except BlockingIOError:
                continue
            
            if time.time()-start_time > 1:
                log.error("Timeout as data is not recieved in 1 second.")
                break
          
        log.debug(f"Data length {len(data)}")

        self.sel.unregister(self.conn)
        self.conn.close()

        self.__insert_data(data)

        self.CONN_COUNTER +=1




    def __insert_data(self,data):
        """
        This private method is used to connect to the Goboat database and insert the data from the xml-file, should only be called by the __read() method.\n
        \n
        ------------
        PARAMETERS\n
        xml: The data from the xml-file or the path to the xml-file.\n 
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """
        log.info("processing data.....")
        safe_data = True
        try:
            data=data.split(b'#')
        except TypeError:
            safe_data=False
            log.error(f"""File: TCPSERVER.py ErrorType: TypeError: The type is {type(data)}""")
        
        if safe_data==True:
            log.debug(f"Data has been split")

            try:
                unit_dict=json.loads(data[0].decode('utf-8'))
                voltage_dict=json.loads(data[1].decode('utf-8'))
                temp_dict=json.loads(data[2].decode('utf-8'))
                
            except json.decoder.JSONDecodeError:
                safe_data=False
                log.error(f"""File: TCPSERVER.py ErrorType: json.decoder.JSONDecodeError Couldn't convert bytes into dictionary""")
    
        if safe_data==True:
            log.debug(f"Data is being converted into dictionaries")
            xml_parser= XmlParser(xsd_path=(self.directory+"/sch_status_data.xsd"), directory=self.directory, unit_dict = unit_dict, voltage_dict=voltage_dict, temp_dict=temp_dict) #inserets the xml data into the xml_parser from the client.
            xml_parser.get_all_data()

            if xml_parser.valid_xml == True:
                log.info(f"XML is valid")
                Goboat = sql.DatabaseConnection(user=self.user,password=self.password,host=self.host, port=3306,database=self.database, directory=self.directory) # establish connection to the database
                input = xml_parser

                Goboat.insert_boat_data(boat_ID=input.boat_id,date=input.date,lok_lat=input.lok_lat,lok_long=input.lok_long,temperatures=input.temp_list,watt=input.watt,voltage_array=input.voltage_list)


    def run(self):
        """
        This method calls the loop that will constantly listen for something on the specified port self.PORT, and makes a queue for clients that is yet to be handled\n
        This method should be called by the user, but is a while True loop, so it will not break.\n
        \n
        ------------
        PARAMETERS\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == "__main__":
    test = SQL_socket(user="testuser",password="testpassword", host="127.0.0.1",database='goboatv2')
    print('* TCP Server listening for incoming connections in port {}'.format(test.PORT))
    test.run()

"""
# Test on Frederik's pc
if __name__ == "__main__":
    test = SQL_socket(user="frederik",password="password", host="127.0.0.1",database='goboatv2',directory="C:/Users/frede/Downloads")
    print('* TCP Server listening for incoming connections in port {}'.format(test.PORT))
    test.run()
"""
