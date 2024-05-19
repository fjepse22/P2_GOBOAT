# Version 1.02 | Encoding UTF_8
# Created by : Jesper Hammer
# Date: 17-05-2024

from machine import ADC
from machine import Pin
from logger import Logger

class DRVBattSensor:
    """
    Handles hardware initialisation and connection as well as fetching data from hardware\n
    List of class methods:\n
    - get: fetches data from hardware(battery sensors)\n
    """

    def __init__(self, log_file) -> None:
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
            #Create sensor object
            self.sensor_0 = ADC(Pin(36))
            self.sensor_1 = ADC(Pin(39))
            self.sensor_2 = ADC(Pin(34))
            self.sensor_3 = ADC(Pin(35))
            self.sensor_4 = ADC(Pin(32))
            self.sensor_5 = ADC(Pin(33))
            self.sensor_6 = ADC(Pin(25))
            self.sensor_7 = ADC(Pin(26))

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

        self.log.debug("Getting battery data")
        try:
            ch_0 = self.sensor_0.read()
            ch_1 = self.sensor_1.read()
            ch_2 = self.sensor_2.read()
            ch_3 = self.sensor_3.read()
            ch_4 = self.sensor_4.read()
            ch_5 = self.sensor_5.read()
            ch_6 = self.sensor_6.read()
            ch_7 = self.sensor_7.read()

            return ch_0, ch_1, ch_2, ch_3, ch_4, ch_5, ch_6, ch_7
        except Exception as e:
            self.log.critical (f"An error occured while initialising sensor input: {e}")