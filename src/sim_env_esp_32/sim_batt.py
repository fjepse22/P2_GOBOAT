# Version 1.07 | Encoding UFT-8
# Created by: Maiken Hammer
# Date: 02-05-2024

import random 
from parser_csv_dict import CSVDictParser
from validator_csv import ValidatorCSV
from logger import Logger

class SimBatt():
    """
    Simulates changes in battery terminal voltage based on battery current charge\n
    List of class methods:\n
    - batt:get: gets current terminal voltage and a random temperature\n
    """

    def __init__(self, log_file:str, file:str, sch_file:str) -> None:
        """
        Initialises the class\n
        \n
        ------------
        PARAMETERS\n
        file:\n
        Takes name of log file of type STRING\n
        File must be of type TXT\n
        Takes name af battery configuration file of type STRING\n
        File must be of type CSV\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        self.log = Logger(__name__, log_file)

        #Validates the configuration against its corresponding schema
        try:
            assert ValidatorCSV.validate(file, sch_file)

        except Exception as e:
            self.log.critical(f"VALUE ERROR in CONSUMER CONFIG file: {e}")

        parser = CSVDictParser(log_file)
        self.batt_def = parser.csv_dict_parser_float(file)
        self.soc_key  = [key for key in self.batt_def]
        
    def batt_get(self, charge:float) -> float:
        """
        Gets current terminal voltage and a random temperature\n
        \n
        ------------
        PARAMETERS\n
        charge:\n
        Takes current charge var of type FLOAT\n
        \n
        ------------
        RETURNS\n
        Returns terminal voltage as return_value var\n
        Return is of type FLOAT\n
        Returns battery temperature\n
        Return is of type INT\n
        \n
        """

        self.log.debug("Fetching actual terminal voltage and battery temperature")

        if charge <= self.soc_key[-1]:
            self.log.error("Battery empty! Ending simulation!")
            raise "Battery empty! Ending simulation!"
        
        else:

            try:
                self.temp = random.randint(40,42)

                #Determines which interval of SOC the current charge belongs to and returns the highest value of the interval
                for _ in range(len(self.soc_key ) -1):
                    if charge <= self.soc_key[_] and charge > self.soc_key[_ +1]:
                        self.return_value = self.batt_def.get(self.soc_key[_])
                        return self.return_value, float(self.temp)
                if charge <= self.soc_key[len(self.soc_key)]:
                    self.return_value = self.batt_def.get(self.soc_key[_])

                return self.return_value, float(self.temp)
            except Exception as e:
                self.log.critical(f"An error occurred while getting battery data: {e}")