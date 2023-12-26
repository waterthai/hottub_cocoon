import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()

class Modbus_Volt():
    def read_volt(self):
        volt_array = []
        client1 = ModbusSerialClient(
                method='rtu',
                port=path_url.modbus_port,
                baudrate=9600,
                timeout=1,
                parity='N',
                stopbits=1,
                bytesize=8
            )
        client1.connect()
        res1 = client1.read_holding_registers(37, 3, path_url.volt_address)
        volt_array.append(res1.registers[0])
        volt_array.append(res1.registers[1])
        volt_array.append(res1.registers[2])
        return volt_array
        
