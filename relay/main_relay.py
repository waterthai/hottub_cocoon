from modbus_relay import Modbus_relay
from urllib.request import urlopen
import json
import sys
import time
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()
url = path_url.url_setting_mode
mod = Modbus_relay()


class Main_relay():
    status_of_relay = ''
    status_filtration = ''
    def __init__(self, status_of_relay, status_filtration):
        self.status_of_relay = status_of_relay
        self.status_filtration = status_filtration
    def start_relay(self):
        print('Start Relay')
    
        response = urlopen(url)
        data_json = json.loads(response.read())
        if self.status_filtration ==  True: 
            if str(data_json[0]['sm_filtration']) != "0":
                read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_auto.txt','r')
                status_read_filtration_auto = read_status_auto.read().rstrip('\n')
                if status_read_filtration_auto == "False":
                    if str(data_json[0]['sm_ozone_choc']) == "1":
                        if self.status_of_relay[2] == False:
                            mod.open_ozone_choc()
                
                    elif str(data_json[0]['sm_ozone_choc']) == "0":
                        if self.status_of_relay[2] == True:
                            mod.close_ozone_choc()
    
                if str(data_json[0]['sm_lamp_ozone']) == "1":
                    if self.status_of_relay[0] == False:
                        mod.open_lamp_ozone()
                # elif data_json[0]['sm_lamp_ozone'] == "2":
                elif str(data_json[0]['sm_lamp_ozone']) == "0":
                    if self.status_of_relay[0] == True:
                        mod.close_lamp_ozone()
                elif str(data_json[0]['sm_lamp_ozone']) == "2":
                    if self.status_of_relay[2] == True:
                        if self.status_of_relay[0] == False:
                            mod.open_lamp_ozone()
                    else :
                        if self.status_of_relay[0] == True:
                            mod.close_lamp_ozone()
                        
                    
                if str(data_json[0]['sm_lamp_uv']) == "1":
                    if self.status_of_relay[1] == False:
                        mod.open_lamp_uv()
                elif str(data_json[0]['sm_lamp_uv']) == "0":
                    if self.status_of_relay[1] == True:
                        mod.close_lamp_uv()
                elif str(data_json[0]['sm_lamp_uv']) == "2":
                    if self.status_of_relay[2] == True:
                        if self.status_of_relay[1] == False:
                            mod.open_lamp_uv()
                    else:
                        if self.status_of_relay[1] == True:
                            mod.close_lamp_uv()

                
                if str(data_json[0]['sm_pump_air']) == "1":
                    if self.status_of_relay[3] == False:
                        # read_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','r')
                        # counter_open_air_pump = int(read_open_air_pump.read())
                        # if counter_open_air_pump < 5:
                        #     sum_counter_open_air_pump = counter_open_air_pump + 1
                        #     write_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','w')
                        #     write_open_air_pump.write(str(sum_counter_open_air_pump))
                        # else:
                            mod.open_pompe_air()
                # elif data_json[0]['sm_pump_air'] == "2":
                elif str(data_json[0]['sm_pump_air']) == "0":
                    if self.status_of_relay[3] == True:
                        # write_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','w')
                        # write_open_air_pump.write("0")
                        mod.close_pompe_air()
                elif str(data_json[0]['sm_pump_air']) == "2":
                    if self.status_of_relay[2] == True:
                        if self.status_of_relay[3] == False:
                            # read_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','r')
                            # counter_open_air_pump = int(read_open_air_pump.read())
                            # if counter_open_air_pump < 5:
                            #     sum_counter_open_air_pump = counter_open_air_pump + 1
                            #     write_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','w')
                            #     write_open_air_pump.write(str(sum_counter_open_air_pump))
                            # else:
                                mod.open_pompe_air()
                    else:
                        # if self.status_of_relay[3] == True:
                        #     write_open_air_pump = open('/home/pi/hottub_ma/txt_file/counter_open_air_pump.txt','w')
                        #     write_open_air_pump.write("0")
                            mod.close_pompe_air()

            else:
                print("----------CLOSE ALL RELAY--------------")
                #close all relay
                if self.status_of_relay[0] == True:
                    mod.close_lamp_ozone()
                if self.status_of_relay[0] == False:    
                    if self.status_of_relay[1] == True:    
                     mod.close_lamp_uv()
                if self.status_of_relay[1] == False:    
                    if self.status_of_relay[2] == True:
                        mod.close_ozone_choc()
                if self.status_of_relay[2] == False:    
                    if self.status_of_relay[3] == True:
                        mod.close_pompe_air()
                if self.status_of_relay[3] == False:    
                    if self.status_of_relay[4] == True:
                        mod.close_besgo()
                if self.status_of_relay[4] == False:   
                    if self.status_of_relay[5] == True: 
                        mod.close_ph()
                if self.status_of_relay[5] == False:    
                    if self.status_of_relay[6] == True:
                        mod.close_orp()
                if self.status_of_relay[6] == False:  
                    if self.status_of_relay[7] == True:  
                        mod.close_apf()
        else:
            print("Close Another Relay")
            if self.status_of_relay[0] == True or  self.status_of_relay[1] == True or  self.status_of_relay[2] == True or  self.status_of_relay[3] == True or  self.status_of_relay[4] == True or  self.status_of_relay[5] == True or  self.status_of_relay[6] == True or  self.status_of_relay[7] == True:
                time.sleep(0.5)
                mod.close_lamp_ozone()
                time.sleep(0.5)
                mod.close_lamp_uv()
                time.sleep(0.5)
                mod.close_ozone_choc()
                time.sleep(0.5)
                mod.close_pompe_air()
                time.sleep(0.5)
                mod.close_besgo()
                time.sleep(0.5)
                mod.close_ph()
                time.sleep(0.5)
                mod.close_orp()
                time.sleep(0.5)
                mod.close_apf()

