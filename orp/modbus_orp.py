import minimalmodbus
import serial
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()
class Modbus_ORP():
    def start_orp(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x06,0xFF,0x00,0x6C,0x3B])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x06\xFF\x00\x6C\x08")
    def stop_orp(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
   
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x06,0x00,0x00,0x2D,0xCB])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x06\x00\x00\x2D\xF8")

    def read_orp_counter(self):
        read_orp = open('./orp/txt_file/counter_orp.txt','r')
        return int(read_orp.read())
    
    def write_orp_counter(self):
        counter_orp = self.read_orp_counter()
        counter_orp += 1
        write_orp = open('./orp/txt_file/counter_orp.txt','w')
        write_orp.write(str(counter_orp))
    def set_orp_counter_zero(self):
        write_orp = open('./orp/txt_file/counter_orp.txt','w')
        write_orp.write("0")

