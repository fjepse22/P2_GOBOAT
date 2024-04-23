import socket
import selectors
#from xml_parser import XmlParser

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
    data = conn.recv(3000) # Should be ready
    #xml_parser= XmlParser(xml_path=str(data, 'UTF-8'),xsd_path="sch_status_data.xsd",xml_from_file=False)
    #xml_parser.get_all_data()
    #print(xml_parser)

    sel.unregister(conn)
    conn.close()
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
