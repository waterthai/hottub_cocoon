from modbus import Modbus
import time
from urllib.request import urlopen
import json
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_ma/relay/')
from modbus_relay import Modbus_relay

path_url = Path_url()
url = path_url.url_setting_mode
url_filtration_time = path_url.url_filtration_time
url_setting = path_url.url_setting


mod = Modbus()
modbus_relay = Modbus_relay()

status_plc_out = ''

class Main_PLC():
    status_relay = ''
    status_filtration = False
    system_datetime = ""
    status_working = 1
    temperature = 0.00
    status_plc = ''

    def __init__(self, system_datetime, temperature, plc, relay_8):
        self.system_datetime = system_datetime
        self.temperature = temperature
        self.status_plc = plc
        self.status_relay = relay_8

    def start_plc(self):
        status_plc_out = self.status_plc
        self.status_filtration = status_plc_out[0]
        #ดึงการตั้งค่าเวลา
        response = urlopen(url)
        data_json = json.loads(response.read())

        #ดึงสถานะการตั้งค่าเวลา filtration
        filtration_time = urlopen(url_filtration_time)
        data_time_status = json.loads(filtration_time.read())

        #ดึงข้อมูล config
        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())


        if data_json[0]['sm_filtration'] == "1":
            write_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_auto.txt','w')
            write_status_auto.write("False")
            if status_plc_out[0] == False:
                mod.start_filtration()
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
            else:
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)

            if str(data_json[0]['sm_ozone_choc']) == "2":
                 self.close_ozone_choc()

            

        elif data_json[0]['sm_filtration'] == "2":     
            print("Filtration Auto Mode")
            #สั่งเปิดเมื่อ เวลาที่ set filtration
            if self.system_datetime >= "00:00" and self.system_datetime <= '00:59':
                self.auto_filtration_working(data_time_status[0], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "01:00" and self.system_datetime <= '01:59':
                self.auto_filtration_working(data_time_status[1], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "02:00" and self.system_datetime <= '02:59':
                self.auto_filtration_working(data_time_status[2], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "03:00" and self.system_datetime <= '03:59':
                self.auto_filtration_working(data_time_status[3], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "04:00" and self.system_datetime <= '04:59':
               self.auto_filtration_working(data_time_status[4], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "05:00" and self.system_datetime <= '05:59':
                self.auto_filtration_working(data_time_status[5], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "06:00" and self.system_datetime <= '06:59':
                self.auto_filtration_working(data_time_status[6], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "07:00" and self.system_datetime <= '07:59':
                self.auto_filtration_working(data_time_status[7], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "08:00" and self.system_datetime <= '08:59':
               self.auto_filtration_working(data_time_status[8], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "09:00" and self.system_datetime <= '09:59':
                self.auto_filtration_working(data_time_status[9], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "10:00" and self.system_datetime <= '10:59':
                self.auto_filtration_working(data_time_status[10], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "11:00" and self.system_datetime <= '11:59':
                self.auto_filtration_working(data_time_status[11], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "12:00" and self.system_datetime <= '12:59':
                self.auto_filtration_working(data_time_status[12], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "13:00" and self.system_datetime <= '13:59':
                self.auto_filtration_working(data_time_status[13], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "14:00" and self.system_datetime <= '14:59':
               self.auto_filtration_working(data_time_status[14], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "15:00" and self.system_datetime <= '15:59':
                self.auto_filtration_working(data_time_status[15], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "16:00" and self.system_datetime <= '16:59':
                self.auto_filtration_working(data_time_status[16], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "17:00" and self.system_datetime <= '17:59':
                self.auto_filtration_working(data_time_status[17], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "18:00" and self.system_datetime <= '18:59':
                self.auto_filtration_working(data_time_status[18], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "19:00" and self.system_datetime <= '19:59':
                self.auto_filtration_working(data_time_status[19], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "20:00" and self.system_datetime <= '20:59':
                self.auto_filtration_working(data_time_status[20], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "21:00" and self.system_datetime <= '21:59':
                self.auto_filtration_working(data_time_status[21], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "22:00" and self.system_datetime <= '22:59':
                self.auto_filtration_working(data_time_status[22], status_plc_out, data_json, data_setting)
            elif self.system_datetime >= "23:00"   and self.system_datetime <= '23:59':
                self.auto_filtration_working(data_time_status[23], status_plc_out, data_json, data_setting)
               
          
        else :
            print("---------Close Filtration---------")
            if status_plc_out[0] == True:
              
                mod.stop_filtration()
            if status_plc_out[0] == False:
                if status_plc_out[1] == True:
                    write_close_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','r')
                    counter_close_ozone_pump = int(write_close_ozone_pump.read())
                    if counter_close_ozone_pump < 5:
                        sum_counter_close_ozone_pump = counter_close_ozone_pump + 1
                        write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                        write_clear_ozone_pump.write(str(sum_counter_close_ozone_pump))
                    else:
                        mod.stop_ozone_pump()
                if status_plc_out[1] == False:
                    mod.stop_chauffage()

    def auto_filtration_working(self, data_time_status,status_plc_out, data_json, data_setting):
        write_status_auto = open('/home/pi/hottub_ma/txt_file/status_working_auto.txt','w')
        write_status_auto.write("True")
        if str(data_time_status) != "0":
            if status_plc_out[0] == False:
                mod.start_filtration()

            if str(data_json[0]['sm_ozone_choc']) == "1":
                self.start_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "2":
                if str(data_time_status) == "2":
                    self.start_ozone_choc()
                else :
                    self.close_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "0":
                self.close_ozone_choc()
        
        else:
            if str(data_json[0]['sm_ozone_choc']) == "1":
                self.start_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "2":
                if str(data_time_status) == "2":
                    self.start_ozone_choc()
                else :
                    self.close_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "0":
                self.close_ozone_choc()
            read_status_heater = open('/home/pi/hottub_ma/txt_file/status_working_heater.txt','r')
            set_heater_text = read_status_heater.read().rstrip('\n')
            print("xxxxxxxxxxx"+str(set_heater_text))
            if str(set_heater_text) == "False":
                if status_plc_out[0] == True:
                    mod.stop_filtration() 
        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)


    def pompe_ozone_and_chauffage(self, status_plc_out, data_json, data_setting):
        print("-------------------pompe ozone and chauffage------------------")
        if status_plc_out[0] == True :
                #pompe zone
                if data_json[0]['sm_pomp_ozone'] != "0" :
                    if str(data_json[0]['sm_pomp_ozone']) == "1":
                        if status_plc_out[1] == False:
                            write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                            write_clear_ozone_pump.write("0")
                            mod.start_ozone_pump()
                    elif str(data_json[0]['sm_pomp_ozone']) == "2" :
                        if self.status_relay[2] == True:
                            if status_plc_out[1] == False:
                                write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                                write_clear_ozone_pump.write("0")
                                mod.start_ozone_pump()
                        else:
                            if status_plc_out[1] == True:
                                write_close_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','r')
                                counter_close_ozone_pump = int(write_close_ozone_pump.read())
                                if counter_close_ozone_pump < 5:
                                    sum_counter_close_ozone_pump = counter_close_ozone_pump + 1
                                    write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                                    write_clear_ozone_pump.write(str(sum_counter_close_ozone_pump))
                                else:
                                    mod.stop_ozone_pump()
                else:
                    if status_plc_out[1] == True :
                        write_close_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','r')
                        counter_close_ozone_pump = int(write_close_ozone_pump.read())
                        if counter_close_ozone_pump < 5:
                            sum_counter_close_ozone_pump = counter_close_ozone_pump + 1
                            write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                            write_clear_ozone_pump.write(str(sum_counter_close_ozone_pump))
                        else:
                            mod.stop_ozone_pump()
        else:
            if status_plc_out[1] == True :
                write_close_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','r')
                counter_close_ozone_pump = int(write_close_ozone_pump.read())
                if counter_close_ozone_pump < 5:
                    sum_counter_close_ozone_pump = counter_close_ozone_pump + 1
                    write_clear_ozone_pump =  open('/home/pi/hottub_ma/txt_file/counter_close_ozone_pump.txt','w')
                    write_clear_ozone_pump.write(str(sum_counter_close_ozone_pump))
                else:
                    mod.stop_ozone_pump()


                #chauffage 
                # if data_json[0]['sm_pomp_ozone'] == "0" :
                #     if data_json[0]['sm_chauffage'] == "1":
                #         if (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) <  float(data_setting[0]['setting_temperature']):
                #             if status_plc_out[2] == False:
                #                 mod.start_chauffage()
                #         elif (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) >=  float(data_setting[0]['setting_temperature']):
                #             if status_plc_out[2] == True:
                #                 mod.stop_chauffage()
                #     else:
                #         if status_plc_out[2] == True:
                #             mod.stop_chauffage()
                      

                # elif data_json[0]['sm_pomp_ozone'] == "1" :
                #     if data_json[0]['sm_chauffage'] == "1":
                #      if status_plc_out[1] == True:
                #         if (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) <  float(data_setting[0]['setting_temperature']):
                #             if status_plc_out[2] == False:
                #                 mod.start_chauffage()
                #         elif (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) >=  float(data_setting[0]['setting_temperature']):
                #             if status_plc_out[2] == True:
                #                 mod.stop_chauffage()
                #     else:
                #         if status_plc_out[2] == True:
                #             mod.stop_chauffage()
                            
    def start_ozone_choc(self):
         if self.status_relay[2] == False:
            modbus_relay.open_ozone_choc()
            
    def close_ozone_choc(self):
        if self.status_relay[2] == True:
            modbus_relay.close_ozone_choc()

    
