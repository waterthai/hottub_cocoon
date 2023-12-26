import minimalmodbus
import serial
from pymodbus.client import ModbusSerialClient
from setting.path_url import Path_url

class Modbus_isaver_hat():
    send = ''
    def __init__(self):
        self.send = serial.Serial(
                port='/dev/ttyS0',
                baudrate = 1200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
       
    def set_freq2900(self):
        #text2900
        self.send.write(b"\xAA\xD0\x0B\xB9\x0B\x54\x0C\xCD")
    
    def set_freq2300(self):
        #txt2300
        self.send.write(b"\xAA\xD0\x0B\xB9\x08\xFC\x0D\x83")

    def set_freq2000(self):
        self.send.write(b"\xAA\xD0\x0B\xB9\x07\xD0\x09\xAE")

    def set_freq1800(self):
        #txt1800
        self.send.write(b"\xAA\xD0\x0B\xB9\x07\x08\x09\xF4")
       

    def close_iserve(self):
        self.send.write(b"\xAA\xD0\x0B\xB9\x00\x01\xCB\xC2")
