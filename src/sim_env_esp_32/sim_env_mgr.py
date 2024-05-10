# Version 1.01 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 01-05-2024
# Modified by: Ib Leminen Mohr Nielsen
# Last Modified: 10-05-2024

import time
from parser_csv_dict import CSVDictParser
from sim_data_pos import Pos
from sim_data_loc_time import SimDataLocTime
from sim_data_pdraw import PDraw
from sim_data_batt import SimDataBatt
from esp_tcpclient import Client
from logger import Logger

class SimEnvMgr:
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
            self.data_batt_def = self.settings.get("config_file_battery")
            self.batt_def = self.parser.csv_dict_parser_float(self.data_batt_def)
            self.soc_key  = [key for key in self.batt_def]
            self.data_unit = {"id" : self.settings.get("unit_id"), "pos_lat" : 3300000, "pos_lon" : -10400000, "time" : 0, "p_draw" : 0}
            self.data_batt_voltage = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, 
                                        "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
            self.data_batt_temp = {"batt_1" : 0, "batt_2" : 0, "batt_3" : 0, "batt_4": 0, 
                                    "batt_5": 0, "batt_6": 0, "batt_7" : 0, "batt_8" : 0}
            self.data_batt_charge = {"batt_1" : self.soc_key[0], "batt_2" : self.soc_key[0], "batt_3" : self.soc_key[0], "batt_4": self.soc_key[0], 
                                    "batt_5": self.soc_key[0], "batt_6": self.soc_key[0], "batt_7" : self.soc_key[0], "batt_8" : self.soc_key[0]}
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


        while run != 0:
            
            #Instantiation of battery and consumer classes
            try:
                batt_1 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_2 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_3 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_4 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_5 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_6 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_7 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                batt_8 = SimDataBatt(self.settings.get("log_file"), self.data_batt_def)
                pd = PDraw(self.settings.get("log_file"), self.settings.get("config_file_consumer"),self.settings.get("schema_file_consumer"))
            except Exception as e:
                self.log.critical(f"An error occurred whilie instantiating: {e}")

            #Creating files for updating data
            self.new_data_pos_lat = {"pos_lat" : Pos.move(self.data_unit.get("pos_lat"), 1)}
            self.new_data_pos_lon = {"pos_lon" : Pos.move(self.data_unit.get("pos_lon"), 1)}
            self.new_data_time = {"time" : SimDataLocTime.time()}
            self.new_data_pdraw = {"p_draw": pd.get(lap_counter)}
            self.new_data_u_batt_1 = {"batt_1" : batt_1.batt_get(self.data_batt_charge.get("batt_1") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_1 = {"batt_1" : batt_1.batt_get(self.data_batt_charge.get("batt_1") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_1 = {"batt_1" : self.data_batt_charge.get("batt_1") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_2 = {"batt_2" : batt_2.batt_get(self.data_batt_charge.get("batt_2") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_2 = {"batt_2" : batt_2.batt_get(self.data_batt_charge.get("batt_2") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_2 = {"batt_2" : self.data_batt_charge.get("batt_2") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_3 = {"batt_3" : batt_3.batt_get(self.data_batt_charge.get("batt_3") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_3 = {"batt_3" : batt_3.batt_get(self.data_batt_charge.get("batt_3") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_3 = {"batt_3" : self.data_batt_charge.get("batt_3") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_4 = {"batt_4" : batt_4.batt_get(self.data_batt_charge.get("batt_4") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_4 = {"batt_4" : batt_4.batt_get(self.data_batt_charge.get("batt_4") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_4 = {"batt_4" : self.data_batt_charge.get("batt_4") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_5 = {"batt_5" : batt_5.batt_get(self.data_batt_charge.get("batt_5") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_5 = {"batt_5" : batt_5.batt_get(self.data_batt_charge.get("batt_5") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_5 = {"batt_5" : self.data_batt_charge.get("batt_5") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_6 = {"batt_6" : batt_6.batt_get(self.data_batt_charge.get("batt_6") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_6 = {"batt_6" : batt_6.batt_get(self.data_batt_charge.get("batt_6") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_6 = {"batt_6" : self.data_batt_charge.get("batt_6") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_7 = {"batt_7" : batt_7.batt_get(self.data_batt_charge.get("batt_7") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_7 = {"batt_7" : batt_7.batt_get(self.data_batt_charge.get("batt_7") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_7 = {"batt_7" : self.data_batt_charge.get("batt_7") - (self.data_unit.get("p_draw") / 8)}
            self.new_data_u_batt_8 = {"batt_8" : batt_8.batt_get(self.data_batt_charge.get("batt_8") - (self.data_unit.get("p_draw") / 8))[0]}
            self.new_data_t_batt_8 = {"batt_8" : batt_8.batt_get(self.data_batt_charge.get("batt_8") - (self.data_unit.get("p_draw") / 8))[1]}
            self.new_data_c_batt_8 = {"batt_8" : self.data_batt_charge.get("batt_8") - (self.data_unit.get("p_draw") / 8)}
            
            #Updating data in dicts
            self.data_unit.update(self.new_data_pos_lat)
            self.data_unit.update(self.new_data_pos_lon)
            self.data_unit.update(self.new_data_time)
            self.data_unit.update(self.new_data_pdraw)
            self.data_batt_voltage.update(self.new_data_u_batt_1)
            self.data_batt_temp.update(self.new_data_t_batt_1)
            self.data_batt_charge.update(self.new_data_c_batt_1)
            self.data_batt_voltage.update(self.new_data_u_batt_2)
            self.data_batt_temp.update(self.new_data_t_batt_2)
            self.data_batt_charge.update(self.new_data_c_batt_2)
            self.data_batt_voltage.update(self.new_data_u_batt_3)
            self.data_batt_temp.update(self.new_data_t_batt_3)
            self.data_batt_charge.update(self.new_data_c_batt_3)
            self.data_batt_voltage.update(self.new_data_u_batt_4)
            self.data_batt_temp.update(self.new_data_t_batt_4)
            self.data_batt_charge.update(self.new_data_c_batt_4)
            self.data_batt_voltage.update(self.new_data_u_batt_5)
            self.data_batt_temp.update(self.new_data_t_batt_5)
            self.data_batt_charge.update(self.new_data_c_batt_5)
            self.data_batt_voltage.update(self.new_data_u_batt_6)
            self.data_batt_temp.update(self.new_data_t_batt_6)
            self.data_batt_charge.update(self.new_data_c_batt_6)
            self.data_batt_voltage.update(self.new_data_u_batt_7)
            self.data_batt_temp.update(self.new_data_t_batt_7)
            self.data_batt_charge.update(self.new_data_c_batt_7)
            self.data_batt_voltage.update(self.new_data_u_batt_8)
            self.data_batt_temp.update(self.new_data_t_batt_8)
            self.data_batt_charge.update(self.new_data_c_batt_8)
            
            #Updating execution data and mannaging timing
            lap_counter += 1
            time.sleep(1/t_scale)
            self.send_data(self.data_unit, self.data_batt_voltage, self.data_batt_temp)
            #print(self.data_unit, self.data_batt_voltage, self.data_batt_temp, self.data_batt_charge)
    
    def send_data(self, unit_dict, voltage_dict, temp_dict):
        """
        Sends data to network GoBoat server\n
        \n
        ------------
        PARAMETERS\n
        unit_dict\n
        voltage_dict\n
        temp_dict\n
        \n
        ------------
        RETURNS\n
        TBD!!!\n
        \n
        """
        client=Client()
        client.send_data(unit_dict, voltage_dict, temp_dict) #to change ip adress of server, change to client.send_data(unit_dict, voltage_dict, temp_dict, "new_ip_adress")  