# Version 1.06 | Encoding UFT-8
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
        local_time = time.ctime(time.time())
        return local_time[11:-5]