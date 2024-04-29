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

"""
This needs to be event based with a que system, in order to ensure that all data gets into the database
"""

class SQL_socket:
    """
    SQL_socket(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None)

    This socket is used to recieve xml-files that are to be inserted into the SQL-server.

    It can only connect to the Goboat database on port 3306.

    Once the object is made it will start to listen on 
    
    """

    def __init__(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None) -> None:
        """
         __init__(self,HOST='',PORT=8888,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None)


         Initialises the object and starts the process to listen
        """


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
        self.sel.register(self.sock, selectors.EVENT_READ, self.__accept)

        #This start the the listening process
        #self.logger=logging.basicConfig(filename='/home/Gruppe250/test/SQL_socket.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

    def __accept(self,sock, mask):
        """
        __accept(self,sock, mask)

        Should not be run by a user.\n
        Used to establish a connection to a client, that sends a xml-file
        
        
        """
        print('accept function is running')
        self.conn, self.addr = self.sock.accept() # Should be ready
        print('accepted', self.conn, 'from', self.addr)
        self.conn.setblocking(False)
        self.sel.register(self.conn, selectors.EVENT_READ, self.__read)


    def __read(self,sock, mask):
        """
        __read(self)
        
        This method is used to recieve the xml-file from a client.\n
        Will after that insert the xml-data into the SQL-database


        """
        print('read function is running')
        data = b''
        while b"EOF" not in data: # runs while EOF(end of file) is not in the data, which is recieved last from the client. 
            try:
                data += self.conn.recv(self.BUFFER_SIZE) # used try except to avoid blocking error
            except BlockingIOError:
                continue  
        self.sel.unregister(self.conn)
        self.conn.close()

        # Creates a XML-file out of the data string and removes the end of file string.
        xml_file= str(data[:-3], 'UTF-8')

        self.__insert_data(xml_file)

        # Threading is not yet implemented

        #event = threading.Event(target=self.insert_data, args=(str(xml_file),),name=f'Insert_xml_thread_{self.CONN_COUNTER}')
       # event.set()
        self.CONN_COUNTER +=1




    def __insert_data(self,xml):
        """
        __insert_data(xml)
        
        This method is used to connect to the Goboat database and insert the data from the xml-file.\n
        This method should only be called by the __read() method.
        
        """
        xml_parser= XmlParser(xsd_path="home/Gruppe250/test/sch_status_data.xsd", xml_path=str(xml)) #inserets the xml data into the xml_parser from the client.

        xml_parser.get_all_data()
        if xml_parser.valdid_xml == True:
            Goboat = sql.DatabaseConnection(user=self.user,password=self.password,host=self.host) # establish connection to the database
            input = xml_parser

            Goboat.insert_boat_data(boat_ID=input.boat_id,Date=input.date,Lok_lat=input.lok_lat,Lok_long=input.lok_long,Battery_temperatures=input.temp_list,Watt_hour=input.watt_hour,Voltage_array=input.voltage_list)


    def run(self):
        """
        run()
        

        This method calls the loop that will constantly listen for something on the specified port self.PORT\n
        Warning!!! This will start an unstoppable while True loop.
        """
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


test = SQL_socket(user="testuser",password="testpassword", host="127.0.0.1")
print('* TCP Server listening for incoming connections in port {}'.format(test.PORT))
test.run()
