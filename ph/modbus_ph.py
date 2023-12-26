import minimalmodbus
import serial
import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()
class Modbus_PH():

    
    def start_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
    
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x05,0xFF,0x00,0x9C,0x3B])
        send.write(data_bytes)

    def stop_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x05,0x00,0x00,0xDD,0xCB])
        send.write(data_bytes)

    def read_ph_counter(self):
        read_ph = open('./ph/txt_file/counter_ph.txt','r')
        return int(read_ph.read())
    
    def write_ph_counter(self):
        counter_ph = self.read_ph_counter()
        counter_ph += 1
        write_ph = open('./ph/txt_file/counter_ph.txt','w')
        write_ph.write(str(counter_ph))
    def set_ph_counter_zero(self):
        write_ph = open('./ph/txt_file/counter_ph.txt','w')
        write_ph.write("0")
