#Version 1.02 | Encoding UTF-8
#Created 23-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 15-05-2024

import socket
import selectors
import time
from logger import log
import sql_insert_data as sql
from xml_parser import XmlParser

class SQL_socket:
    """
    This socket is used to recieve xml-files that are to be inserted into the SQL-server.\n
    It can only connect to the Goboat database on port 3306.\n
    Once the object is made it will start to listen on. \n
    \n
    
    List of class methods:\n
    - __init__(self,HOST='',PORT=9999,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None): Initialises the object and starts the process to listen\n

    - __accept_connection(self,sock, mask): Used to establish a connection to a client, that sends a xml-file.\n

    - __read_data(self, sock, mask): This method is used to recieve the xml-data from a client and insert it into the database\n

    - __insert_data(self,xml):  This method is used to connect to the Goboat database and insert the data from the xml-file, should only be called by the __read_data() method. \n

    - run(self): This method calls the loop that will constantly listen for something on the specified port self.PORT\n
    """

    def __init__(self,HOST='',PORT=9999,CONN_COUNTER=0,BUFFER_SIZE=1024,user= None,password= None,host = None, directory="/home/Gruppe250/Server",database='goboatv2') -> None:
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
        self.database = database                #the name of the database

        #Creates sockets
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.__accept_connection)

        #This start the the listening process

    def __accept_connection(self,sock, mask):
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
        conn, addr = self.sock.accept() # Should be ready
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.__read_data)
    

    def __read_data(self, conn, mask): 
        """
        This private method is used to read, recieve and store data\n
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
        self.CONN_COUNTER += 1
        log.debug(f"Connection number {self.CONN_COUNTER} has been established")
        self.start_time = time.time()

        # Recieves the header max 3 bytes ie ((2^24)-1) length of data
        header=self.__recieved_data(conn, 3)
        if header is None:
            self.sel.unregister(conn)
            conn.close()
            log.debug(f"Connection number {self.CONN_COUNTER} has been closed")
            return
        log.debug(f"header length {int.from_bytes(header, 'big')}")
        
        # Recieves the data, using the length of the data as buffer size
        data=self.__recieved_data(conn, int.from_bytes(header, 'big'))
        if data is None:
            self.sel.unregister(conn)
            conn.close()
            log.debug(f"Connection number {self.CONN_COUNTER} has been closed")
            return
        log.debug(f"data length {len(data)}")

        # Creates a XML-file out of the data.
        self.__insert_data(data)

        # Unregisters the socket and closes the connection
        self.sel.unregister(conn)
        conn.close()
        log.debug(f"Connection number {self.CONN_COUNTER} has been closed")
        
    def __recieved_data(self,conn, data_size, timeout=1):
        """
        This private method is used to reacieve data\n
        \n
        ------------
        PARAMETERS\n
        conn: Used for connecting to client.\n
        data_size: Legth of incomming message.\n
        timeout: Specified timeout for while loop if it doesnt close.\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "data": The incomming data from a client\n
        Return type Bytes\n
        """
        data = b''
        while len(data) < data_size:
            try:
                current_data = conn.recv(data_size-len(data)) # forces the buffer to be the size of data_size
                if not current_data:
                    log.error(f"Connection closed by client")
                    return None
                data += current_data
            except BlockingIOError:
                continue
            if time.time() - self.start_time >= timeout:
                log.error(f"Timeout as data is not recieved in {timeout}s.")
                return None
        return data




    def __insert_data(self,xml):
        """
        This private method is used to connect to the Goboat database and insert the data from the xml-file, should only be called by the __read_data() method.\n
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
        try:
            xml=str(xml, 'utf-8')
        except Exception as e:
            log.error(f"Error decoding the data: {e}")
            return

        xml_parser= XmlParser(xsd_path=(self.directory+"/sch_status_data.xsd"), xml_input=xml, directory=self.directory) #inserets the xml data into the xml_parser from the client.

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

