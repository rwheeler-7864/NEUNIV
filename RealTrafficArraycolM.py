from interface import implements
from LightArray import *
import wiringpi as wiringpi
#NUMBER OF COLUMNS
NUMCOL=8
NUMROW=9
class RealTrafficArray(implements(LightArray)):
    def __init__(self):
	wiringpi.mcp23017Setup(101, 0x20)       # set up the pins and i2c address  
        wiringpi.mcp23017Setup(117, 0x24)      # set up second MCP23017 - not used in single config test 
        wiringpi.mcp23017Setup(133, 0x22)      # set up second MCP23017 - not used in single config test
        wiringpi.mcp23017Setup(149, 0x26)      # set up second MCP23017 - not used in single config test
        wiringpi.mcp23017Setup(165, 0x21)


	for x in range (101,173):
		wiringpi.pinMode(x, 1)     
		wiringpi.digitalWrite(x, 1)

    def turnOn(self, x, y):
       	wiringpi.digitalWrite((x * NUMROW + y) + 101, 0)  

    def turnOff(self, x, y):
       	wiringpi.digitalWrite((x * NUMROW + y) + 101, 1)  
 
    def getWidth(self):
	return NUMCOL

    def getHeight(self):
	return NUMROW

    def cleanup(self):
	for i in range(101, 173):
	    wiringpi.digitalWrite(i, 1)
