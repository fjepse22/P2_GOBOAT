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

    def send_data(self, message, server_ip="192.168.1.10", server_port=9999, nbytes=3):
        """
        Sends data to the server.
        \n
        ------------
        PARAMETERS\n
        \n
        message: The message to be sent.\n
        server_ip: The IP of the server. Default is 192.168.1.10"
        server_port: The port of the server. Default is 9999.\n
        nbytes: The number of bytes to be sent. Default is 3.\n
        \n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return type is None.\n
        """
        
        
        s = socket(AF_INET,SOCK_STREAM)

        try:
            s.connect((server_ip, server_port))
        except ConnectionRefusedError: 
            print(f"{ConnectionRefusedError}, the connection was refused")
            pass    

        try:
            header=len(message)
            s.send(header.to_bytes(nbytes, 'big'))
            s.send(message)
            print(header)

        except OverflowError:
            print(f"{OverflowError}, the message is too long")
            
        except BrokenPipeError:
            print(f"{BrokenPipeError}, the connection is broken")
        
        s.close()


if __name__ == "__main__":
    message = b'<status_data><boatData><ID>1</ID><PositionLat>33.00001</PositionLat><PositionLon>-103.99999</PositionLon><Time>17:54:33</Time></boatData><battData><Battery1><Voltage>12.89</Voltage><Temperature>42.0</Temperature></Battery1><Battery2><Voltage>12.89</Voltage><Temperature>42.0</Temperature></Battery2><Battery3><Voltage>12.89</Voltage><Temperature>42.0</Temperature></Battery3><Battery4><Voltage>12.89</Voltage><Temperature>42.0</Temperature></Battery4><Battery5><Voltage>12.89</Voltage><Temperature>41.0</Temperature></Battery5><Battery6><Voltage>12.89</Voltage><Temperature>41.0</Temperature></Battery6><Battery7><Voltage>12.89</Voltage><Temperature>42.0</Temperature></Battery7><Battery8><Voltage>12.89</Voltage><Temperature>40.0</Temperature></Battery8><Draw>0.001388888888888889</Draw></battData></status_data>'
    
    client = TCPClient()
    client.send_data(message, server_ip="192.168.1.140", server_port=9999)# Change the IP to the IP of the server
