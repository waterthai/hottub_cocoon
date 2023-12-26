import serial
import sys
from setting.path_url import Path_url
sys.path.append('/home/pi/hottub_ma/relay/')
from modbus_relay import Modbus_relay


path_url = Path_url()
modbus_relay = Modbus_relay()
class Modbus_besgo():
    def open_besgo(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0D,0xFF,0x00,0x1D,0xF9])
            send.write(data_bytes)
        except:
            pass
        # self.send.write(b"\x02\x05\x00\x04\xFF\x00\xCD\xC8")

    def close_besgo(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0D,0x00,0x00,0x5C,0x09])
            send.write(data_bytes)
        except:
            pass
        # self.send.write(b"\x02\x05\x00\x04\x00\x00\x8C\x38")

    def close_all_working(self, status_relay):
        try:
            if status_relay[0] == True:
                modbus_relay.close_lamp_ozone()
            if status_relay[0] == False:    
                if status_relay[1] == True:    
                    modbus_relay.close_lamp_uv()
            if status_relay[1] == False:    
                if status_relay[2] == True:
                    modbus_relay.close_ozone_choc()
            if status_relay[2] == False:    
                if status_relay[3] == True:
                    modbus_relay.close_pompe_air()
            # if status_relay[3] == False:    
            #     if status_relay[5] == True: 
            #         modbus_relay.close_ph()
            # if status_relay[4] == False:   
            #     if status_relay[6] == True:
            #         modbus_relay.close_orp()
            # if status_relay[5] == False:    
            #     if status_relay[7] == True:  
            #         modbus_relay.close_apf()
        except:
            pass


            


