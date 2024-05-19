# Version 1.00 | Encoding UTF_8
# Created by : Maiken Lanng
# Date: 27-04-2024

class SimPos():
    """
    A class to move a cordinate 
    List of class methods:\n
    - move: moves the cordinate by 0.0001\n
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def move(pos:int, move:int) -> int:
            
        """
        Moves the cordinate by 1\n
        \n
        ------------- 
        PARAMETERS\n
        \n
        pos: 
        Takes any INT\n
        move:\n
        Takes any INT\n
        -------------
        RETURNS\n
        \n
        Returns pos\n
        Return type is INT
        """

        pos = int(pos) + int(move)

        return int(pos)