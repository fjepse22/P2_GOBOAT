# Version 1.00 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 04-05-2024

from logger import Logger
import xml.etree.ElementTree as ET

class XMLDictParser:
    """
    Parses .xml-files and returns dict\n
    List of class methods:\n
    - csv_dict_parser_str: parses csv-file to dict containing str variable(s)\n
    """

    def __init__(self, log_file) -> None:
        """
        Initialises the logger\n
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


    def xml_dict_parser_str(self, in_file: str) -> dict:

        """
        Parses xml-file to dict containing str variable(s)\n
        \n
        ------------
        PARAMETERS\n
        in_file:\n
        Takes input file name of type STRING\n
        File must be of type XML\n
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
        try:
            tree = ET.parse(in_file)
            root = tree.getroot()

            for child in root:
                add_data = {child.tag : child.text}
                return_file.update(add_data)
            return return_file
                
        except Exception as e:
            self.log.error (f"An error occured while parsing XML: {e}")