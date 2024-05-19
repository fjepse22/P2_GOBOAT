# Version 1.07 | Encoding UFT-8
# Created by: Maiken Hammer
# Date: 27-04-2024

from parser_csv_lst import CSVLstParser
from validator_csv import ValidatorCSV
from logger import Logger

class SimPDraw():
    """
    Simulates power consumption based on descriptive configuration file\n
    List of class methods:\n
    - get: gets current terminal consumption in Watts\n
    """

    def __init__(self,log_file:str, file:str, sch_file:str) -> None:
        """
        Initialises the class\n
        \n
        ------------
        PARAMETERS\n
        log_file:\n
        Takes log file name of type STRING\n
        File must be of type TXT\n
        file:\n
        Takes configuration file name of type STRING\n
        File must be of type CSV\n
        sch_file:\n
        Takes schema file name of type STRING\n
        File must be of type CSV\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        self.log = Logger(__name__, log_file)
        self.parser = CSVLstParser(log_file)
        self.profile = []
        self.factor = 0
        self.consumption_over_time = []

        #Validates the configuration against its corresponding schema
        try:
            assert ValidatorCSV.validate(file, sch_file)

        except Exception as e:
            self.log.critical(f"VALUE ERROR in CONSUMER CONFIG file: {e}")

        #Opens and parses file obj to list
        self.profile = self.parser.csv_lst_parser(file)

        #Resolves power consumption over time list
        for i in self.profile:
            if str(i[1]) == "s":
                self.factor = 1
            elif str(i[1]) == "m":
                self.factor = 60
            elif str(i[1]) == "h":
                self.factor = 360

            for _ in range(int(i[0]) * self.factor):
                self.consumption_over_time.append(int(i[2]) / 3600)
            
            self.factor = 0

        self.consumption_over_time.append("EOF")
    
    def get(self, iter:int) -> int:
        """
        Gets current terminal consumption in Watts\n
        \n
        ------------
        PARAMETERS\n
        iter:\n
        Takes current iteration var of type INT\n
        \n
        ------------
        RETURNS\n
        Returns current consumption in Watts\n
        Return is of type INT\n
        \n
        """

        self.log.info("Fetching actual consumption")
        try:
            return self.consumption_over_time[iter]
        
        except IndexError:
            return 0