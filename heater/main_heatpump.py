import json
import sys
import time
from urllib.request import urlopen
from modbus_heater import Modbus_heatpump
sys.path.append('/home/pi/hottub_ma/relay/')
from modbus_relay import Modbus_relay
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_ma/plc/')
from modbus import Modbus


path_url = Path_url()
url_setting = path_url.url_setting
url = path_url.url_setting_mode
url_heatpump = path_url.url_heatpump
mod_heatpump = Modbus_heatpump()
modbus_relay  = Modbus_relay()
plc_mod = Modbus()


class Main_HeatPump():

    def start_heatpump(self,  temperature, plc, relay_8,status_heatpump):
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%H", named_tuple)

        response_heatpump = urlopen(url_heatpump)
        data_heatpump = json.loads(response_heatpump.read())
        hour_start = data_heatpump[0]['heatpump_start']
        hour_end = data_heatpump[0]['heatpump_end']
        split_hour_start = hour_start.split(':')
        split_hour_end = hour_end.split(':')
        if int(time_string) >= int(split_hour_start[0])  and int(time_string) < int(split_hour_end[0]) :
            if plc[2] == True:
                mod_heatpump.stop_chauffage()
                time.sleep(0.5)
                mod_heatpump.stop_chauffage2()
                time.sleep(0.5)
                self.clear_heater_open_count()

            response_setting = urlopen(url_setting)
            data_setting = json.loads(response_setting.read())

            setting = urlopen(url)
            data_mode = json.loads(setting.read())
            if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                if str(data_mode[0]['sm_filtration']) != "0":
                    if str(data_mode[0]['sm_chauffage']) == "1":
                        if plc[0] == False:
                            plc_mod.start_filtration()
                    read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                    read_status_auto.write("True")
                    if status_heatpump == False:
                     mod_heatpump.start_y14()
            elif float(data_setting[0]['setting_temperature']) <= float(temperature):
                read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                read_status_auto.write("False")
                if status_heatpump == True:
                    mod_heatpump.stop_y14()


        else:
            if status_heatpump == True:
                    mod_heatpump.stop_y14()
            if relay_8[4] == False:
                response_setting = urlopen(url_setting)
                data_setting = json.loads(response_setting.read())

                setting = urlopen(url)
                data_mode = json.loads(setting.read())
                if str(data_mode[0]['sm_filtration']) != "0":
                    if str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == True:
                        set_temp = float(data_setting[0]['setting_temperature'])
                        temp_div = float(data_setting[0]['setting_temp_deff'])
                        read = float(temperature)
                        print(set_temp)
                        print(temp_div)
                        print(read)

                        # minus = float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff'])
                        if  float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                            print("เปิดปั้ม")
                            read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                            read_status_auto.write("True")
                            # read_counter_open = open('/home/pi/hottub_ma/txt_file/counter_open_heater.txt','r')
                            # counter_open_heater = int(read_counter_open.read())
                            # if counter_open_heater < 60 :
                            #     sum_counter_heater = counter_open_heater + 1
                            #     write_counter_open = open('/home/pi/hottub_ma/txt_file/counter_open_heater.txt','w')
                            #     write_counter_open.write(str(sum_counter_heater))
                            # else:
                            if plc[2] == False:
                                mod_heatpump.start_chauffage()
                            if plc[2] == True:
                                mod_heatpump.start_chauffage2()
                        elif float(temperature) >= float(data_setting[0]['setting_temperature']): 
                            print("ปิดปั้ม")
                            read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                            read_status_auto.write("False")
                            if plc[2] == True:
                                mod_heatpump.stop_chauffage()
                                time.sleep(0.5)
                                mod_heatpump.stop_chauffage2()
                                time.sleep(0.5)
                                self.clear_heater_open_count()
                            # if plc[2] == False:
                            #     if plc[3] == True:
                            #         mod_heatpump.stop_chauffage2()
                    elif str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == False:
                        set_temp = float(data_setting[0]['setting_temperature'])
                        temp_div = float(data_setting[0]['setting_temp_deff'])
                        read = float(temperature)
                        print(set_temp)
                        print(temp_div)
                        print(read)
                        if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >  float(temperature):
                            read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                            read_status_auto.write("True")
                            if plc[0] == False:
                                plc_mod.start_filtration()
                        # else :
                        elif float(temperature) >= float(data_setting[0]['setting_temperature']):
                            print("ปิดปั้ม")
                            read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                            read_status_auto.write("False")
                            if plc[2] == True:
                                mod_heatpump.stop_chauffage()
                                time.sleep(0.5)
                                mod_heatpump.stop_chauffage2()
                                time.sleep(0.5)
                                self.clear_heater_open_count()
                            # if plc[2] == False:
                            #     if plc[3] == True:
                            #         mod_heatpump.stop_chauffage2()
                    else:
                        read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                        read_status_auto.write("False")
                        if plc[2] == True:
                            mod_heatpump.stop_chauffage()
                            time.sleep(0.5)
                            mod_heatpump.stop_chauffage2()
                            time.sleep(0.5)
                            self.clear_heater_open_count()
                        # if plc[2] == False:
                        #     if plc[3] == True:
                        #         mod_heatpump.stop_chauffage2()
                else:
                    read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                    read_status_auto.write("False")
                    if plc[2] == True:
                        mod_heatpump.stop_chauffage()
                        time.sleep(0.5)
                        mod_heatpump.stop_chauffage2()
                        time.sleep(0.5)
                        self.clear_heater_open_count()
                    # if plc[2] == False:
                    #     if plc[3] == True:
                    #         mod_heatpump.stop_chauffage2()

            else:
                read_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','w')
                read_status_auto.write("False")
                if plc[2] == True:
                    mod_heatpump.stop_chauffage()
                    time.sleep(0.5)
                    mod_heatpump.stop_chauffage2()
                    time.sleep(0.5)
                    self.clear_heater_open_count()
                # if plc[2] == False:
                #     if plc[3] == True:
                #         mod_heatpump.stop_chauffage2()
                    
                if plc[2] == False:
                    if plc[1] == True:
                        mod_heatpump.stop_pump_ozone()
    def clear_heater_open_count(self):
        write_counter_open = open('/home/pi/hottub_ma/txt_file/counter_open_heater.txt','w')
        write_counter_open.write("0")

        
