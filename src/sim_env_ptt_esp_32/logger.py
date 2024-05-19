# Version 1.06 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 06-05-2024

import time

class Logger:
    """
    Appends log enty to selected file when prompted\n
    List of class methods:\n
    - write: writes contents of message var to file\n
    - clear_log: clears contents of existing log\n
    - debug: creates message var for debug level entry
    - info: creates message var for info level entry
    - warning: creates message var for warning level entry
    - error: creates message var for error level entry
    - critical: creates message var for critical level entry
    """
    def __init__(self, name:str, file:str) -> None:
        """
        Initialises the class\n
        \n
        ------------
        PARAMETERS\n
        name:\n
        Takes name af instantiating file of type STRING\n
        file:\n
        Takes name of log file of type STRING\n
        File must be of type TXT\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        self.log_file = file
        self.caller_name = name
        self.get_time = f"{time.localtime()[2]}/{time.localtime()[1]}-{time.localtime()[0]} {time.localtime()[3]}:{time.localtime()[4]}:{ time.localtime()[5]}"

    def write(self, msg:str) -> None:
        """
        Writes contents of message var to file\n
        \n
        ------------
        PARAMETERS\n
        msg:\n
        Takes message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        with open(self.log_file,'a') as writer:
            writer.write(f"\n{msg}")
            writer.close()

    def clear_log(self) -> None:
        """
        Clears contents of existing log\n
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
        
        with open(self.log_file,'w') as writer:
            writer.write("")
            writer.close()

    def debug(self, input:str) -> None:
        """
        Creates message var for debug level entry
        \n
        ------------
        PARAMETERS\n
        input:\n
        Takes input for message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        message = (f"DEBUG : {self.caller_name} : {self.get_time} : {input}")
        self.write(message)

    def info(self, input:str) -> None:
        """
        Creates message var for info level entry
        \n
        ------------
        PARAMETERS\n
        input:\n
        Takes input for message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        message = (f"INFO : {self.caller_name} : {self.get_time} : {input}")
        self.write(message)

    def warning(self, input:str) -> None:
        """
        Creates message var for warning level entry
        \n
        ------------
        PARAMETERS\n
        input:\n
        Takes input for message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        message = (f"WARNING : {self.caller_name} : {self.get_time} : {input}")
        self.write(message)

    def error(self, input:str) -> None:
        """
        Creates message var for error level entry
        \n
        ------------
        PARAMETERS\n
        input:\n
        Takes input for message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        message = (f"ERROR : {self.caller_name} : {self.get_time} : {input}")
        self.write(message)
        
    def critical(self, input:str) -> None:
        """
        Creates message var for critical level entry
        \n
        ------------
        PARAMETERS\n
        input:\n
        Takes input for message var of type STRING\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        message = (f"CRITICAL : {self.caller_name} : {self.get_time} : {input}")
        self.write(message)