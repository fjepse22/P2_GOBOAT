#Version 1.00 | Encoding UTF-8
#Created by: Jesper Hammer
#Date: 26/04-2024
# Modified 14-05-2024
# Modified by: Frederik B. B. Jepsen

import json
import logging.config
import logging

# use 
# from logging import log 
# in order to use the log functoin here.

class logger:
    """
    Class with method for configuration of logging functionality\n
    List of class methods:\n
    - __init__: Gets and sets class global vars\n
    - setup: Imports and applies config file for logging functionality\n
    """

    def __init__(self, log_type: str) -> None:
        """
        Gets and sets class global vars\n
        ------------
        PARAMETERS\n
        \n
        log_type\n
        Takes any STR\n
        ------------
        RETURNS\n
        \n
        None\n
        """

        #Setting global var
        self.__logger_type__ = log_type

    def setup(self) -> str:
        """
        Imports and applies config file for logging functionality\n
        ------------
        PARAMETERS\n
        \n
        None\n
        ------------
        RETURNS\n
        \n
        self.__logger_type__\n
        Return type is STR\n
        """

        #Opening and parsing json file
        try:
            with open("/home/Gruppe250/test/log_config.json") as file_in:
                config = json.load(file_in)
        #Prints error message to terminal, if file is not found, since log is not yet instantiated
        except FileNotFoundError as e:
            print("Configuration file for logging module not found. Exiting.\n %s", e)
        
        #Passes config file to logging module
        logging.config.dictConfig(config)
        return self.__logger_type__
    
logger_setup = logger("dev")
logger_setup.setup()

log = logging.getLogger(logger_setup.__logger_type__)
#log.info("info test")
