""""test client, used together with TCPSERVER.py to test the server"""

from socket import *

SERVER_IP = "192.168.1.10"
SERVER_PORT = 8888
BUFFER_SIZE = 1024


s = socket(AF_INET,SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))


file = open("status_data.xml", "rb")
encoded_string = file.read(BUFFER_SIZE)

while encoded_string:
    s.send(encoded_string)
    encoded_string = file.read(BUFFER_SIZE)

file.close()
s.send(b'EOF')
s.close()
print("Data sent.")


