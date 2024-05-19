# Version 1.01 | Encoding UFT-8
# Created by: Maiken Hammer
# Date: 27-04-2024
# Modified by: Ib Leminen Mohr Nielsen
# Last Modified: 10-05-2024

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
    def time() -> str:

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
        if time.localtime()[3] < 10:
            hour = "0"+str(time.localtime()[3])
        else:
            hour = str(time.localtime()[3])
        
        if time.localtime()[4] < 10:
            minute = "0"+str(time.localtime()[4])
        else:
            minute = str(time.localtime()[4])
        
        if time.localtime()[5] < 10:
            second = "0"+str(time.localtime()[5])
        else:
            second = str(time.localtime()[5])

        return f"{hour}:{minute}:{second}"