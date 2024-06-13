# Version 1.02 | Encoding UTF_8
# Created by : Jesper Hammer
# Date: 16-05-2024

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from logger import Logger

class DRVBattSensor:
    """
    Handles hardware initialisation and connection as well as fetching data from hardware\n
    List of class methods:\n
    - get: fetches data from hardware(battery sensors)\n
    """

    def __init__(self, log_file:str) -> None:
        """
        Initialises the class and sets op configuration\n
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

        self.log.info("Initialising sensor assets")

        try:    

            # create the spi bus
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

            # create the cs (chip select)
            cs = digitalio.DigitalInOut(board.D5)

            # create the mcp object
            self.mcp = MCP.MCP3008(spi, cs)

        except Exception as e:
            self.log.critical (f"An error occured while initialising firmware assets: {e}")

    def get(self):
        """
        Fetches data from hardware(battery sensors)\n
        \n
        ------------
        PARAMETERS\n
        None\n
        \n
        ------------
        RETURNS\n
        Returns a list of sensor values\n
        Return is of type LIST\n
        List elements is of type FLOAT\n
        \n
        """

        ret_0 = 0
        ret_1 = 0
        ret_2 = 0
        ret_3 = 0
        ret_4 = 0
        ret_5 = 0
        ret_6 = 0
        ret_7 = 0

        self.log.debug("Getting battery data")
        try:
            # create analog input channels
            self.ch_0 = AnalogIn(self.mcp, MCP.P0)
            self.ch_1 = AnalogIn(self.mcp, MCP.P1)
            self.ch_2 = AnalogIn(self.mcp, MCP.P2)
            self.ch_3 = AnalogIn(self.mcp, MCP.P3)
            self.ch_4 = AnalogIn(self.mcp, MCP.P4)
            self.ch_5 = AnalogIn(self.mcp, MCP.P5)
            self.ch_6 = AnalogIn(self.mcp, MCP.P6)
            self.ch_7 = AnalogIn(self.mcp, MCP.P7)

            return self.ch_0, self.ch_1, self.ch_2, self.ch_3, self.ch_4, self.ch_5, self.ch_6, self.ch_7
        except Exception as e:
            self.log.critical (f"An error occured while initialising sensor input: {e}")