import serial
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
from pymodbus.client import ModbusSerialClient

path_url = Path_url()

class Modbus_heatpump():
    def read_heatpump_plc(self):
        try:
            status_plc_out = []
            client = ModbusSerialClient(
                    method='rtu',
                    port=path_url.modbus_port,
                    baudrate=9600,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            client.connect()
            res = client.read_coils(512, 4, path_url.plc_address2)
            status_plc_out.append(res.bits[0])
            status_plc_out.append(res.bits[1])
            status_plc_out.append(res.bits[2])
            status_plc_out.append(res.bits[3])
            return status_plc_out
        except:
            pass

    def open_heatpump(self):
        try:
            heatpump = serial.Serial(
                    port=path_url.modbus_port,
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)
            heatpump.write(b"\x06\x05\x02\x01\xFF\x00\xDD\xF5")
            heatpump.close()
        except:
            pass
        
    def close_heatpump(self):
        try:
            send = serial.Serial(
                    port=path_url.modbus_port,
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)
            send.write(b"\x06\x05\x02\x01\x00\x00\x9C\x05")
            send.close()
        except:
            pass

    def start_chauffage(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x02,0xFF,0x00,0x2D,0xFA])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x02\xFF\x00\x26\xB2")
        except:
            pass

    def stop_chauffage(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x02,0x00,0x00,0x6C,0x0A])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x02\x00\x00\x67\x42")
        except:
            pass
    def stop_pump_ozone(self):
        try:
            ozone = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x26,0x01,0x00,0x00,0x97,0x42])
            ozone.write(data_bytes)
            # ozone.write(b"\x01\x05\x26\x01\x00\x00\x97\x42")
            # ozone.close()
        except:
            pass

    def start_chauffage2(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x03,0xFF,0x00,0x7C,0x3A])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\xFF\x00\x77\x72")
        except:
            pass

    def stop_chauffage2(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x03,0x00,0x00,0x3D,0xCA])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\x00\x00\x36\x82")
        except:
            pass

    def start_y14(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0E,0xFF,0x00,0xED,0xF9])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\x00\x00\x36\x82")
        except:
            pass
    
    def stop_y14(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0E,0x00,0x00,0xAC,0x09])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\x00\x00\x36\x82")
        except:
            pass

    def start_y15(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0F,0xFF,0x00,0xBC,0x39])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\x00\x00\x36\x82")
        except:
            pass

    def stop_y15(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x00,0x0F,0x00,0x00,0xFD,0xC9])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x03\x00\x00\x36\x82")
        except:
            pass

