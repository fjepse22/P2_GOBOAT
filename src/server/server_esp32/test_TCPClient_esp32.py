""""test client, used together with TCPSERVER.py to test the server"""
from socket import *
import json
import time

class TCPClient:
    def __init__(self):
        pass

    def payload(self, unit_dict, voltage_dict, temp_dict, nbytes=3, message=None, server_ip="192.168.1.10", server_port=8888):
        byte_unit_dict=json.dumps(unit_dict).encode('utf-8')+b'#'
        byte_voltage_dict=json.dumps(voltage_dict).encode('utf-8')+b'#'
        byte_temp_dict=json.dumps(temp_dict).encode('utf-8')+b'#'
        
        if message == None:
            message = byte_unit_dict+byte_voltage_dict+byte_temp_dict
            self.send_data(message, server_ip, server_port, nbytes)
        else:
            self.send_data(message, server_ip, server_port, nbytes)

    def send_data(self, message, SERVER_IP, SERVER_PORT, nbytes):
        """
        Sends data to the server.
        \n
        ------------
        PARAMETERS\n
        \n
        data_unit_dict: Dictionary with the data from the unit.
        data_batt_voltage_dict: Dictionary with the battery voltage data.
        data_batt_temp_dict: Dictionary with the battery temperature data.
        \n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return type is None.\n
        """
        s = socket(AF_INET,SOCK_STREAM)
        start_time = time.time()

        try:
            s.connect((SERVER_IP, SERVER_PORT))
        except (ConnectionRefusedError, OSError) as e: 
            print(f"{e}, the connection was refused")
            return    

        try:
            header=len(message)
            s.send(header.to_bytes(nbytes, 'big'))
            s.send(message)
            print('header', header)
            #print(message)

        except (Exception) as e:
            print(f"{e}")
        
        s.close()



if __name__ == "__main__":
    local_time = time.ctime(time.time())
    
    unit_dict = {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : local_time[11:-5], "p_draw" : 1}
    voltage_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    temp_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

    # some inputs used for testing stability of server
    input_list=["hello", 1, ["hello", "hello", "hello"], None, True, {"t":1}]
    #for i in range(0, len(input_list)):
        #client = TCPClient()
        #client.payload(unit_dict, voltage_dict, temp_dict, nbytes=3, message=input_list[i])
    
    #client = TCPClient()
    for i in range(10):
        client = TCPClient()
        client.payload(unit_dict, voltage_dict, temp_dict, nbytes=3, server_ip="192.168.1.10", server_port=8888)# Change the IP to the IP of the server

