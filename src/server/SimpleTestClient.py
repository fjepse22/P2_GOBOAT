#Version 1.00 | Encoding UTF-8
#Created 23-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 14-05-2024

""""test client, used together with TCPSERVER.py to test the server"""
from socket import *

class TCPClient:
    def __init__(self):
        pass

    def payload(self, file):
        """
        Reads the file and returns the message.
        \n
        ------------
        PARAMETERS\n
        \n
        file: The file that contains the data to be sent to the server.\n
        \n
        ------------
        RETURNS\n
        \n
        Returns the message\n
        Return type is bytes.\n
        """
        
        with open(file, "rb") as message:
            message = message.read()
        return message

    def send_data(self, file="status_data.xml", SERVER_IP="192.168.1.10", SERVER_PORT=8888):
        """
        Sends data to the server.
        \n
        ------------
        PARAMETERS\n
        \n
        file: The file that contains the data to be sent to the server. Default is "status_data.xml".\n
        SERVER_IP: The IP of the server. Default is 192.168.1.10"
        SERVER_PORT: The port of the server. Default is 8888.\n
        \n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return type is None.\n
        """
        message=self.payload(file)
        
        s = socket(AF_INET,SOCK_STREAM)

        try:
            s.connect((SERVER_IP, SERVER_PORT))
        except ConnectionRefusedError: 
            print(f"{ConnectionRefusedError}, the connection was refused")
            pass    

        try:
            header=len(message)
            s.send(header.to_bytes(3, 'big'))
            s.send(message)

        except OverflowError:
            print(f"{OverflowError}, the message is too long")
            
        except BrokenPipeError:
            print(f"{BrokenPipeError}, the connection is broken")
        
        s.close()


if __name__ == "__main__":
    client = TCPClient()
    client.send_data(SERVER_IP="192.168.1.140")# Change the IP to the IP of the server
