# Version 1.00 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 18-05-2024

from logger import Logger

class CSVLstParser:
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

    def csv_lst_parser(self, in_file: str) -> list:

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
            return reader
        except Exception as e:
            self.log.critical (f"An error occured while parsing CSV: {e}")