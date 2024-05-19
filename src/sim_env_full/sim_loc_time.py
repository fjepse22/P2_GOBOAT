# Version 1.00 | Encoding UFT-8
# Created by: Maiken Hammer
# Date: 27-04-2024

import time

class SimLocTime():
    """
    A class to log the time\n
    List of class methods:\n
    - time: returns the current time\n
    """


    def __init__(self) -> str:
        pass

    @staticmethod
    def time():

        """
        Returns the current time\n
        \n
        ------------- 
        PARAMETERS\n
        \n
        Takes None\n
        \n
        -------------
        RETURNS\n
        \n
        Returns a string of times\n
        Return type is string\n
        """

        return f"{time.localtime()[2]}/{time.localtime()[1]}-{time.localtime()[0]} {time.localtime()[3]}:{time.localtime()[4]}:{ time.localtime()[5]}"