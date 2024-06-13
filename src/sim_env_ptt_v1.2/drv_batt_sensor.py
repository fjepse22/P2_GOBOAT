import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class DRVMcp300x:
    def __init__(self) -> None:
        pass
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        mcp = MCP.MCP3008(spi, cs)

        self.channel0 = AnalogIn(mcp, MCP.P0)
        self.channel1 = AnalogIn(mcp, MCP.P1)
        self.channel2 = AnalogIn(mcp, MCP.P2)
        self.channel3 = AnalogIn(mcp, MCP.P3)
        self.channel4 = AnalogIn(mcp, MCP.P4)
        self.channel5 = AnalogIn(mcp, MCP.P5)
        self.channel6 = AnalogIn(mcp, MCP.P6)
        self.channel7 = AnalogIn(mcp, MCP.P7)

    


    def decode_val(self, sensor_val):
        voltage_max = 12.89
        voltage_min = 11.63
        sensor_range_max = 65535
        inc_unit = (voltage_max - voltage_min)/sensor_range_max

        return int(((sensor_val*inc_unit) + voltage_min) * 10)
        

    def get(self):
        r_val=[]
        r_val.append(self.decode_val(self.channel0.value))
        r_val.append(self.decode_val(self.channel1.value))
        r_val.append(self.decode_val(self.channel2.value))
        r_val.append(self.decode_val(self.channel3.value))
        r_val.append(self.decode_val(self.channel4.value))
        r_val.append(self.decode_val(self.channel5.value))
        r_val.append(self.decode_val(self.channel6.value))
        r_val.append(self.decode_val(self.channel7.value))
        return r_val