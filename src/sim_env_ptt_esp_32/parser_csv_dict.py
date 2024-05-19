# Version 1.06 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 02-05-2024

from logger import Logger

class CSVDictParser:
    """
    Parses .csv-files and returns dict with selected type\n
    List of class methods:\n
    - csv_dict_parser_float: parses csv-file to dict containing float variable(s)\n
    - csv_dict_parser_str: parses csv-file to dict containing str variable(s)\n
    """

    def __init__(self, log_file) -> None:
        """
        Initialises the logger
        \n
        ------------
        PARAMETERS\n
        log_file:\n
        Takes log file name of type STRING\n
        File must be of type TXT\n
        \n
        ------------
        RETURNS\n
        Returns None\n
        \n
        """

        self.log = Logger(__name__, log_file)

    def csv_dict_parser_float(self, in_file: str) -> dict:

        """
        Parses csv-file to list containing float variable(s)\n
        \n
        ------------
        PARAMETERS\n
        in_file:\n
        Takes input file name of type STRING\n
        File must be of type CSV\n
        \n
        ------------
        RETURNS\n
        Returns a dict of values\n
        Return is of type DICT\n
        List elements is of type FLOAT\n
        \n
        """

        return_file = {}

        #OPEN FILE AND CREATE READER OBJ
        reader = []
        delim = ','

        try:
            with open(in_file,'r') as file:
                for line in file:
                    reader.append(line.rstrip('\n').rstrip('\r').split(delim))

                self.log.debug(f"opened {in_file}")
                #PARSE DATA FROM CSV TO DICT
                for line in reader:
                    add_data = {float(line[0]) : float(line[1])}
                    return_file.update(add_data)
            return return_file
        except Exception as e:
            self.log.critical (f"An error occured while parsing CSV: {e}")


    def csv_dict_parser_str(self, in_file: str) -> dict:

        """
        Parses csv-file to dict containing str variable(s)\n
        \n
        ------------
        PARAMETERS\n
        in_file:\n
        Takes input file name of type STRING\n
        File must be of type CSV\n
        \n
        ------------
        RETURNS\n
        Returns a dict of values\n
        Return is of type DICT\n
        List elements is of type STR\n
        \n
        """

        return_file = {}

        #OPEN FILE AND CREATE READER OBJ
        reader = []
        delim = ','

        try:
            with open(in_file,'r') as file:
                for line in file:
                    reader.append(line.rstrip('\n').rstrip('\r').split(delim))
                
                self.log.debug(f"opened {in_file}")
                #PARSE DATA FROM CSV TO DICT
                for line in reader:
                    add_data = {line[0] : line[1]}
                    return_file.update(add_data)
            return return_file
        except Exception as e:
            self.log.error (f"An error occured while parsing CSV: {e}")