import serial
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()
class Modbus_APF():
        
    def start_apf(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x07,0xFF,0x00,0x3D,0xFB])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x07\xFF\x00\x3D\xC8")
    def stop_apf(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.plc_address,0x05,0x00,0x07,0x00,0x00,0x7C,0x0B])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x07\x00\x00\x7C\x38")

    def read_apf_counter(self):
        read_ph = open('./apf/txt_file/counter_apf.txt','r')
        return int(read_ph.read())
    
    def write_ph_counter(self):
        counter_ph = self.read_apf_counter()
        counter_ph += 1
        write_ph = open('./apf/txt_file/counter_apf.txt','w')
        write_ph.write(str(counter_ph))
    def set_ph_counter_zero(self):
        write_ph = open('./apf/txt_file/counter_apf.txt','w')
        write_ph.write("0")
