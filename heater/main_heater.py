import json
import sys
import time
from urllib.request import urlopen
from modbus_heater import Modbus_heatpump
sys.path.append('/home/pi/hottub_cocoon/relay/')
from modbus_relay import Modbus_relay
sys.path.append('/home/pi/hottub_cocoon/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_cocoon/plc/')
from modbus import Modbus


path_url = Path_url()
url_setting = path_url.url_setting
url = path_url.url_setting_mode
mod_heatpump = Modbus_heatpump()
modbus_relay  = Modbus_relay()
plc_mod = Modbus()


class Main_Heater():

    def start_heater(self,  temperature, plc, relay_8):
        if relay_8[4] == False:
            response_setting = urlopen(url_setting)
            data_setting = json.loads(response_setting.read())

            setting = urlopen(url)
            data_mode = json.loads(setting.read())
            if str(data_mode[0]['sm_filtration']) != "0":
                with open('/home/pi/txt_file/status_besgo.txt','r')  as read_status_besgo:
                    status_besgo = read_status_besgo.readline().strip()
                if status_besgo == "False":
                    if str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == True:
                        # minus = float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff'])
                        if  float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                           
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("True")
                                read_status_auto.close()
                            # with open('/home/pi/txt_file/counter_open_heater.txt','r') as read_counter_open:
                            #     counter_open_heater = read_counter_open.readline().strip()
                            # if float(counter_open_heater) >= 60 :
                            if plc[2] == False:
                                mod_heatpump.start_chauffage()
                            if plc[2] == True:
                                mod_heatpump.start_chauffage2()

                        elif float(temperature) >= float(data_setting[0]['setting_temperature']): 
                          
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("False")
                            if plc[2] == True:
                                mod_heatpump.stop_chauffage()
                                time.sleep(0.5)
                                mod_heatpump.stop_chauffage2()
                                time.sleep(0.5)
                                self.clear_heater_open_count()
                           
                    elif str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == False:
       
                        if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >  float(temperature):
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("True")
                            if plc[0] == False:
                                plc_mod.start_filtration()
                        else :
                          
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("False")
                            if plc[2] == True:
                                mod_heatpump.stop_chauffage()
                                time.sleep(0.5)
                                mod_heatpump.stop_chauffage2()
                                time.sleep(0.5)
                                self.clear_heater_open_count()
                           
                    else:
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                        if plc[2] == True:
                            mod_heatpump.stop_chauffage()
                            time.sleep(0.5)
                            mod_heatpump.stop_chauffage2()
                            time.sleep(0.5)
                            self.clear_heater_open_count()
                        
                else:
                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                        read_status_auto.write("False")
                    if plc[2] == True:
                        mod_heatpump.stop_chauffage()
                        time.sleep(0.5)
                        mod_heatpump.stop_chauffage2()
                        time.sleep(0.5)
                        self.clear_heater_open_count()
                           
            else:
                with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                    read_status_auto.write("False")
                if plc[2] == True:
                    mod_heatpump.stop_chauffage()
                    time.sleep(0.5)
                    mod_heatpump.stop_chauffage2()
                    time.sleep(0.5)
                    self.clear_heater_open_count()
              

        else:
            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                read_status_auto.write("False")
            if plc[2] == True:
                mod_heatpump.stop_chauffage()
                time.sleep(0.5)
                mod_heatpump.stop_chauffage2()
                time.sleep(0.5)
                self.clear_heater_open_count()
                
            if plc[2] == False:
                if plc[1] == True:
                    mod_heatpump.stop_pump_ozone()
    def clear_heater_open_count(self):
        with open('/home/pi/txt_file/counter_open_heater.txt','w') as write_counter_open:
            write_counter_open.write("0")

        
