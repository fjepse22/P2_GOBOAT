""""test client, used together with TCPSERVER.py to test the server"""
from socket import *
import json

class TCPClient:
    def __init__(self):
        pass

    def payload(self, unit_dict, voltage_dict, temp_dict):
        byte_unit_dict=json.dumps(unit_dict).encode('utf-8')+b'#'
        byte_voltage_dict=json.dumps(voltage_dict).encode('utf-8')+b'#'
        byte_temp_dict=json.dumps(temp_dict).encode('utf-8')+b'#'
        
        message = byte_unit_dict+byte_voltage_dict+byte_temp_dict
        return message

    def send_data(self, unit_dict, voltage_dict, temp_dict, SERVER_IP="192.168.1.10", SERVER_PORT=8888):
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
        message=self.payload(unit_dict, voltage_dict, temp_dict)
        
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
    unit_dict = {"id" : 1, "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : "14:12:10", "p_draw" : 0}
    voltage_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    temp_dict = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
    
    client = TCPClient()
    client.send_data(unit_dict, voltage_dict, temp_dict, SERVER_IP="192.168.1.140")# Change the IP to the IP of the server
