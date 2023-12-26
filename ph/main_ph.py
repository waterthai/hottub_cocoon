from urllib.request import urlopen
import json
import sys
from setting.path_url import Path_url
from  modbus_ph import Modbus_PH
sys.path.append('/home/pi/hottub_ma/orp/')
from modbus_orp import Modbus_ORP
sys.path.append('/home/pi/hottub_ma/apf/')
from modbus_apf import Modbus_APF

path_url = Path_url()
url_substance = path_url.url_substance
url_ph = path_url.url_ph
url_orp = path_url.url_orp
url_apf = path_url.url_apf

modbus_ph = Modbus_PH()
modbus_orp = Modbus_ORP()
modbus_apf = Modbus_APF()

class Main_PH():
    current_time = ''
    counter_ph = 0 
    counter_orp = 0
    counter_apf = 0
    read_ph_address = 0
    read_orp_address = 0
    set_relay = ''
    def __init__(self, current_time, set_ph, set_orp, set_relay):
        self.current_time = current_time
        self.read_ph_address = set_ph
        self.read_orp_address = set_orp
        self.set_relay = set_relay

    def start_ph(self):
        print('-------start PH ORP APF-------')
        #load setting ph
        response_ph_setting = urlopen(url_substance)
        ph_json = json.loads(response_ph_setting.read())

        #load time ph
        response_ph = urlopen(url_ph)
        data_ph = json.loads(response_ph.read())

        #load time orp
        response_orp = urlopen(url_orp)
        data_orp = json.loads(response_orp.read())

        #load time apf
        response_apf = urlopen(url_apf)
        data_apf = json.loads(response_apf.read())
        
        #read status 8 relay
        relay8 = self.set_relay

        if self.current_time >= "00:00" and self.current_time <= '00:59':
            self.process_woking(data_ph[0]['ph_1'], ph_json, relay8, data_orp[0]['orp_1'], data_apf[0]['apf_1'])
        elif self.current_time >= "01:00" and self.current_time <= '01:59':
            self.process_woking(data_ph[0]['ph_2'], ph_json, relay8, data_orp[0]['orp_2'], data_apf[0]['apf_2'])
        elif self.current_time >= "02:00" and self.current_time <= '02:59':
            self.process_woking(data_ph[0]['ph_3'], ph_json, relay8, data_orp[0]['orp_3'], data_apf[0]['apf_3'])
        elif self.current_time >= "03:00" and self.current_time <= '03:59':
            self.process_woking(data_ph[0]['ph_4'], ph_json, relay8, data_orp[0]['orp_4'], data_apf[0]['apf_4'])
        elif self.current_time >= "04:00" and self.current_time <= '04:59':
            self.process_woking(data_ph[0]['ph_5'], ph_json, relay8, data_orp[0]['orp_5'], data_apf[0]['apf_5'])
        elif self.current_time >= "05:00" and self.current_time <= '05:59':
            self.process_woking(data_ph[0]['ph_6'], ph_json, relay8, data_orp[0]['orp_6'], data_apf[0]['apf_6'])
        elif self.current_time >= "06:00" and self.current_time <= '06:59':
            self.process_woking(data_ph[0]['ph_7'], ph_json, relay8, data_orp[0]['orp_7'], data_apf[0]['apf_7'])
        elif self.current_time >= "07:00" and self.current_time <= '07:59':
            self.process_woking(data_ph[0]['ph_8'], ph_json, relay8, data_orp[0]['orp_8'], data_apf[0]['apf_8'])
        elif self.current_time >= "08:00" and self.current_time <= '08:59':
           self.process_woking(data_ph[0]['ph_9'], ph_json, relay8, data_orp[0]['orp_9'], data_apf[0]['apf_9'])
        elif self.current_time >= "09:00" and self.current_time <= '09:59':
            self.process_woking(data_ph[0]['ph_10'], ph_json, relay8, data_orp[0]['orp_10'], data_apf[0]['apf_10'])
        elif self.current_time >= "10:00" and self.current_time <= '10:59':
            self.process_woking(data_ph[0]['ph_11'], ph_json, relay8, data_orp[0]['orp_11'], data_apf[0]['apf_11'])
        elif self.current_time >= "11:00" and self.current_time <= '11:59':
            self.process_woking(data_ph[0]['ph_12'], ph_json, relay8, data_orp[0]['orp_12'], data_apf[0]['apf_12'])
        elif self.current_time >= "12:00" and self.current_time <= '12:59':
            self.process_woking(data_ph[0]['ph_13'], ph_json, relay8, data_orp[0]['orp_13'], data_apf[0]['apf_13'])
        elif self.current_time >= "13:00" and self.current_time <= '13:59':
            self.process_woking(data_ph[0]['ph_14'], ph_json, relay8, data_orp[0]['orp_14'], data_apf[0]['apf_14'])
        elif self.current_time >= "14:00" and self.current_time <= '14:59':
            self.process_woking(data_ph[0]['ph_15'], ph_json, relay8, data_orp[0]['orp_15'], data_apf[0]['apf_15'])
        elif self.current_time >= "15:00" and self.current_time <= '15:59':
            self.process_woking(data_ph[0]['ph_16'], ph_json, relay8, data_orp[0]['orp_16'], data_apf[0]['apf_16'])
        elif self.current_time >= "16:00" and self.current_time <= '16:59':
            self.process_woking(data_ph[0]['ph_17'], ph_json, relay8, data_orp[0]['orp_17'], data_apf[0]['apf_17'])
        elif self.current_time >= "17:00" and self.current_time <= '17:59':
            self.process_woking(data_ph[0]['ph_18'], ph_json, relay8, data_orp[0]['orp_18'], data_apf[0]['apf_18'])
        elif self.current_time >= "18:00" and self.current_time <= '18:59':
           self.process_woking(data_ph[0]['ph_19'], ph_json, relay8, data_orp[0]['orp_19'], data_apf[0]['apf_19'])
        elif self.current_time >= "19:00" and self.current_time <= '19:59':
          self.process_woking(data_ph[0]['ph_20'], ph_json, relay8, data_orp[0]['orp_20'], data_apf[0]['apf_20'])
        elif self.current_time >= "20:00" and self.current_time <= '20:59':
            self.process_woking(data_ph[0]['ph_21'], ph_json, relay8, data_orp[0]['orp_21'], data_apf[0]['apf_21'])
        elif self.current_time >= "21:00" and self.current_time <= '21:59':
            self.process_woking(data_ph[0]['ph_22'], ph_json, relay8, data_orp[0]['orp_22'], data_apf[0]['apf_22'])
        elif self.current_time >= "22:00" and self.current_time <= '22:59':
            self.process_woking(data_ph[0]['ph_23'], ph_json, relay8, data_orp[0]['orp_23'], data_apf[0]['apf_23'])
        elif self.current_time >= "23:00" and self.current_time <= '23:59':
            self.process_woking(data_ph[0]['ph_24'], ph_json, relay8, data_orp[0]['orp_24'], data_apf[0]['apf_24'])

    def process_woking(self, data_ph, ph_json, relay8, data_orp, data_apf):
        if data_ph == "1":
            self.process_ph(ph_json, relay8)
        else:
            if relay8[5] == True:
                modbus_ph.stop_ph()
        if data_orp == "1":
            self.process_orp(ph_json, relay8)
        else:
            if relay8[6] == True:
                modbus_orp.stop_orp()
        if data_apf == "1":
            self.process_apf(ph_json, relay8)
        else:
            if relay8[7] == True:
                modbus_apf.stop_apf()

    def process_ph(self, ph_json, relay8):
        read_ph = self.read_ph_address
        #อ่าน สถานะ relay
        relay8 = relay8
     
    
        if float(read_ph) >= float(ph_json[0]['ph_set']):
            # print("------------counter ph start---------------"+str(modbus_ph.read_ph_counter()))
            if int(modbus_ph.read_ph_counter()) == 0:
                # print("------------counter ph start---------------"+str(relay8[5]))
                if relay8[5] == False:
                    # print("------------counter ph start---------+++++++++++++++++++------")
                    modbus_ph.start_ph()
                modbus_ph.write_ph_counter()
            else :
                if relay8[5] == True:
                    modbus_ph.stop_ph()
                modbus_ph.write_ph_counter()
            if int(modbus_ph.read_ph_counter()) >= (int(ph_json[0]['ph_freq']) * 60)  :
            # if int(modbus_ph.read_ph_counter()) >= 10 :
                modbus_ph.set_ph_counter_zero()
                
        elif float(read_ph) <= float(ph_json[0]['ph_lower']):
            if relay8[5] == True:
                modbus_ph.stop_ph()
                modbus_ph.set_ph_counter_zero()

    def process_orp(self, orp_json,relay8):
        read_orp = self.read_orp_address
        #อ่าน สถานะ relay
        relay8 = relay8
        if float(read_orp) <= float(orp_json[0]['orp_set']):
            if modbus_orp.read_orp_counter() == 0:
                if relay8[6] == False:
                    modbus_orp.start_orp()
                modbus_orp.write_orp_counter()
            else :
                if relay8[6] == True:
                    modbus_orp.stop_orp()
                modbus_orp.write_orp_counter()
            #แปลงค่า ครึ่งวิให้เป็น วิ * 2
            if int(modbus_orp.read_orp_counter()) >= (int(orp_json[0]['orp_freq']) * 60) :
            # if int(modbus_orp.read_orp_counter())  >= 10 :
                modbus_orp.set_orp_counter_zero()
        elif float(read_orp) >= float(orp_json[0]['orp_lower']):
            if relay8[6] == True:
                modbus_orp.stop_orp()
                modbus_orp.set_orp_counter_zero()

    def process_apf(self, apf_json,relay8):
        relay8 = relay8
        if modbus_apf.read_apf_counter() == 0:
            if relay8[7] == False:
                modbus_apf.start_apf()
            modbus_apf.write_ph_counter()
        else :
            if relay8[7] == True:
                modbus_apf.stop_apf()
            modbus_apf.write_ph_counter()
            #แปลงค่า ครึ่งวิให้เป็น วิ * 2
        if (float(apf_json[0]['apf_freq']) * 60) == modbus_apf.read_apf_counter() :
            modbus_apf.set_ph_counter_zero()
