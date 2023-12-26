import minimalmodbus
import serial
import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
import requests

path_url = Path_url()

class Modbus_read():
    def read_pressure(self,data_setting):
        try:
            volt_set = 0
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.plc_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1  
            volt = instrument.read_register(7)
            string_volt = str(volt)
            len_string = len(string_volt)
            len_decimal = len_string - 1
            if len_decimal < 3:
                string_integer = string_volt[0:len_decimal -2]
                string_dec = string_volt[0 : 2]
                data_set = '0.'+string_dec
                if data_setting[0]['pressure_type'] == "plus":
                    volt_set = float(data_set) + float(data_setting[0]['pressure_calibrate'])
                else:
                    volt_set = float(data_set) - float(data_setting[0]['pressure_calibrate'])
            else:
                string_integer = string_volt[0:len_decimal -2]
                string_dec = string_volt[1 : 3]
                data_set = string_integer+'.'+string_dec
                if data_setting[0]['pressure_type'] == "plus":
                    volt_set = float(data_set) + float(data_setting[0]['pressure_calibrate'])
                else:
                    volt_set = float(data_set) - float(data_setting[0]['pressure_calibrate'])
            data_psi = ((volt_set - 0.48) * 1.25) 
         
            return data_psi
        except:
            pass
    
    def read_status_relay(self):
        try:
            status_relay = []
            client1 = ModbusSerialClient(
                    method='rtu',
                    port=path_url.modbus_port,
                    baudrate=9600,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            client1.connect()
            data = client1.read_coils(0, 15, path_url.plc_address)
           
            status_relay.append(data.bits[4])
            status_relay.append(data.bits[10])
            status_relay.append(data.bits[11])
            status_relay.append(data.bits[12])
            status_relay.append(data.bits[13])
            status_relay.append(data.bits[5])
            status_relay.append(data.bits[6])
            status_relay.append(data.bits[7])
            return status_relay   
        except:
            pass
    def read_status_plc_in(self):
        try:
            status_plc_in = []
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
            res = client.read_discrete_inputs(0, 15,path_url.plc_address)
            #temp
            status_plc_in.append("False")
            #pressure
            status_plc_in.append("False")
            #night time
            status_plc_in.append(res.bits[0])
            #ozone 1
            status_plc_in.append(res.bits[1])
            #ozone 2
            status_plc_in.append(res.bits[2])
            #UV
            status_plc_in.append(res.bits[3])
            #heater 1
            status_plc_in.append(res.bits[4])
            #heater 2
            status_plc_in.append(res.bits[5])
            return status_plc_in
        except:
            pass

    def read_status_plc_out(self):
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
            data = client.read_coils(0, 15, path_url.plc_address)
            status_plc_out.append(data.bits[0])
            status_plc_out.append(data.bits[1])
            status_plc_out.append(data.bits[2])
            status_plc_out.append(data.bits[3])
            return status_plc_out
        except:
            pass
    
    def read_temperature(self, data_setting):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.plc_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1  
            temp =  instrument.read_register(6)
            string_volt = str(temp)
            print("string_volt"+str(string_volt))
            len_string = len(string_volt)
            print(len_string)
            len_decimal = len_string - 1
            string_integer = string_volt[0:len_decimal -2]
            string_dec = string_volt[1 : 3]
            volt_set = string_integer+'.'+string_dec
            #2.51 = 26.3
            tempset = 0
            if data_setting[0]['temp_type'] == "plus":
               tempset =  (((float(volt_set) + float(data_setting[0]['temp_calibrate']))  * 100) - 113.91) / 4.84
            else:
              tempset =  (((float(volt_set) - float(data_setting[0]['temp_calibrate']))  * 100) - 113.91) / 4.84
            return tempset
        except:
            pass

    
    def read_ph(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.ph_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1
            read_ph1 =  instrument.read_register(2)
            read_ph2 =  instrument.read_register(3)
            request = requests.get("http://localhost:8080/process_ph_orp?data1="+str(read_ph1)+"&data2="+str(read_ph2))
            return request.text
        except:
            pass

    def read_orp(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.orp_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1
            read_ph2=  instrument.read_register(2)
            read_ph3 =  instrument.read_register(3)
            request = requests.get("http://localhost:8080/process_ph_orp?data1="+str(read_ph2)+"&data2="+str(read_ph3))

            return request.text
        except:
            pass
    def read_heatpump(self):
        try:
            client1 = ModbusSerialClient(
                    method='rtu',
                    port=path_url.modbus_port,
                    baudrate=9600,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            client1.connect()
            data = client1.read_coils(0, 15, path_url.plc_address)
           
            status_heatpump = data.bits[14]
           
            return status_heatpump   
        except:
            pass

