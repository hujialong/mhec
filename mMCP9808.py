# Demo MicroPython Class for MCP9808 Temperature Sensor
# Version 0.1
# Disclaimer: This is not an official Splunk solution and with no liability. Use at your own risk.
# For feedback and bug report, please send to jyung@splunk.com

from machine import Pin, I2C

MCP9808_I2C_ADDR = 0x18
MCP9808_REG_TEMP = 0x05
MCP9808_REG_MID = 0x06
MCP9808_MID = 0x0054
MCP9808_REG_DID = 0x07
MCP9808_DID = 0x0400

pin_scl = 5
pin_sda = 4

class mMCP9808(object):

    def __init__(self):
        try:
            self.i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda))
        except:
            return False

    def start(self, sda=pin_sda, scl=pin_scl, addr=MCP9808_I2C_ADDR):
        mid = int(''.join('{:02x}'.format(x) for x in list(self.i2c.readfrom_mem(MCP9808_I2C_ADDR,MCP9808_REG_MID,2))),16)
        did = int(''.join('{:02x}'.format(x) for x in list(self.i2c.readfrom_mem(MCP9808_I2C_ADDR,MCP9808_REG_DID,2))),16)
        if (mid == MCP9808_MID) and (did == MCP9808_DID):
            return True
        else:
            return False

    def getTemp(self):
        return (int(''.join('{:02x}'.format(x) for x in list(self.i2c.readfrom_mem(MCP9808_I2C_ADDR, MCP9808_REG_TEMP,2))),16) & 0x0FFF)/16
