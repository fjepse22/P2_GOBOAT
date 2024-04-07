import socket
import selectors
import time 

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 1024  # Receive Buffer size (power of 2)
sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    
def read(conn, mask):
    data = conn.recv(1000) # Should be ready
    local_time = time.ctime(time.time())
  
    with open ('log.txt', 'a') as file: #creates log.txt and appends the data, time.
        file.write(str(data, 'utf-8')+" "+ local_time +" "+ ('\n'))
      
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
