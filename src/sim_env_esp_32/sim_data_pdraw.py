# Version 1.00 | Encoding UFT-8
# Created by: Maiken Hammer
# Date: 27-04-2024
# Modified by: Jesper Hammer
# Date: 04/05-2024

from validator_csv import ValidatorCSV
from logger import Logger

class PDraw():
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
        self.profile = []
        delim = ','
        self.factor = 0
        self.consumption_over_time = []

        #Validates the configuration against its corresponding schema
        try:
            assert ValidatorCSV.validate(sch_file, file)

        except Exception as e:
            self.log.critical(f"VALUE ERROR in CONSUMER CONFIG file: {e}")

        #Opens and parses file obj to list
        with open(file,'r') as file:
            for line in file:
                self.profile.append(line.rstrip('\n').rstrip('\r').split(delim))

        #Resolves power consumption over time list
        for i in self.profile:
            match str(i[1]):
                case "s":
                    self.factor = 1
                case "m":
                    self.factor = 60
                case "h":
                    self.factor = 360

            for _ in range(int(i[0]) * self.factor):
                self.consumption_over_time.append(int(i[2]))
            
            self.factor = 0
    
    def get(self, iter):
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

        self.log.info("PDraw.get running")
        try:
            return self.consumption_over_time[iter]
        
        except IndexError:
            return 0