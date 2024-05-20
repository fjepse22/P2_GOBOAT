# Version 1.08 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 17-05-2024


import time
from parser_csv_dict import CSVDictParser
from sim_pos import SimPos
from sim_loc_time import SimLocTime
from drv_batt_sensor import DRVBattSensor
from esp_tcpclient import Client
from logger import Logger

class EnvMgr:
    """
    Handles execution of simulation enviroment as well as data storage and -passing\n
    List of class methods:\n
    - send_data: Sends data to network client\n
    - run_sim: executs simulation and handles timescaling\n
    """

    def __init__(self) -> None:
        """
        Initialises the class and sets op configuration and data dicts\n
        \n
        ------------
        PARAMETERS\n
        Takes None\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        initialisation_log = "log.txt"
        self.parser = CSVDictParser(initialisation_log)
        self.log = Logger(__name__, initialisation_log)
        self.log.clear_log()
        self.settings = self.parser.csv_dict_parser_str("setting_sim_env.csv")
        try:
            self.batt_config = int(self.settings.get("total_number_of_batteries")) * \
                                                        (int(self.settings.get("parallel_configuration")[0])/int(self.settings.get("parallel_configuration")[2]))
            #Dict for storing unit data for transmission during collection
            self.data_unit = {"id" : self.settings.get("unit_id"), "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : 0, "p_draw" : 0}
            #Dict for storing battery voltage data for transmission during collection
            self.data_batt_voltage = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, 
                                        "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
            #Dict for storing battery temperature data for transmission during collection
            self.data_batt_temp = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, 
                                    "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}

        except Exception as e:
            self.log.critical(f"An error occurred whilie initializing sim_env_mgr: {e}")

    def run_sim(self) -> None:
        """
        Executs simulation and handles timescaling\n
        \n
        ------------
        PARAMETERS\n
        Takes None\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """
        
        self.log.info("Sim started")
        t_scale = int(self.settings.get("time_scale"))
        lap_counter = 0
        run = 1

        #Instantiation of battery and consumer classes
        try:
            batt = DRVBattSensor(self.settings.get("log_file"))
        except Exception as e:
            self.log.critical(f"An error occurred whilie instantiating: {e}")

        while run != 0:

            #Creating files for updating data
            self.new_data_pos_lat = {"pos_lat" : SimPos.move(self.data_unit.get("pos_lat"), 1)}
            self.new_data_pos_lon = {"pos_lon" : SimPos.move(self.data_unit.get("pos_lon"), 1)}
            self.new_data_time = {"time" : SimLocTime.time()}
            self.new_data_u_batt_1 = {"batt_1" : batt.get()[0]}
            self.new_data_u_batt_2 = {"batt_2" : batt.get()[1]}
            self.new_data_u_batt_3 = {"batt_3" : batt.get()[2]}
            self.new_data_u_batt_4 = {"batt_4" : batt.get()[3]}
            self.new_data_u_batt_5 = {"batt_5" : batt.get()[4]}
            self.new_data_u_batt_6 = {"batt_6" : batt.get()[5]}
            self.new_data_u_batt_7 = {"batt_7" : batt.get()[6]}
            self.new_data_u_batt_8 = {"batt_8" : batt.get()[7]}
            
            #Updating data in dicts
            self.data_unit.update(self.new_data_pos_lat)
            self.data_unit.update(self.new_data_pos_lon)
            self.data_unit.update(self.new_data_time)
            self.data_batt_voltage.update(self.new_data_u_batt_1)
            self.data_batt_voltage.update(self.new_data_u_batt_2)
            self.data_batt_voltage.update(self.new_data_u_batt_3)
            self.data_batt_voltage.update(self.new_data_u_batt_4)
            self.data_batt_voltage.update(self.new_data_u_batt_5)
            self.data_batt_voltage.update(self.new_data_u_batt_6)
            self.data_batt_voltage.update(self.new_data_u_batt_7)
            self.data_batt_voltage.update(self.new_data_u_batt_8)
            
            #Updating execution data and mannaging timing
            lap_counter += 1
            time.sleep(1/t_scale)
            self.send_data(self.data_unit, self.data_batt_voltage, self.data_batt_temp)
            #print(self.data_unit, self.data_batt_voltage, self.data_batt_temp)
    
    def send_data(self, unit_dict, voltage_dict, temp_dict):
        """
        Sends data to network GoBoat server\n
        \n
        ------------
        PARAMETERS\n
        unit_dict: Dictionary for storing unit data\n
        voltage_dict: Dictionary for storing battery voltage data\n
        temp_dict: Dictionary for storing battery temperture data\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """
        client=Client(unit_dict, voltage_dict, temp_dict)
        client.payload() #to change ip adress of server, change to client.send_data(unit_dict, voltage_dict, temp_dict, "new_ip_adress")  