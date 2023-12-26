from modbus import Modbus
import time
from urllib.request import urlopen
import json
from setting.path_url import Path_url
from relay.modbus_relay import Modbus_relay

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
            if status_plc_out[0] == False:
                mod.start_filtration()
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
            else:
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)

        elif data_json[0]['sm_filtration'] == "2":     
            print("Filtration Auto Mode")
            #สั่งเปิดเมื่อ เวลาที่ set filtration
            if self.system_datetime >= "00:00" and self.system_datetime <= '00:59':
                if data_time_status[0] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[0] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "01:00" and self.system_datetime <= '01:59':
                if data_time_status[1] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[1] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "02:00" and self.system_datetime <= '02:59':
                if data_time_status[2] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[2] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "03:00" and self.system_datetime <= '03:59':
                if data_time_status[3] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[3] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "04:00" and self.system_datetime <= '04:59':
                if data_time_status[4] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[4] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "05:00" and self.system_datetime <= '05:59':
                if data_time_status[5] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[5] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "06:00" and self.system_datetime <= '06:59':
                if data_time_status[6] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[6] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "07:00" and self.system_datetime <= '07:59':
                if data_time_status[7] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[7] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "08:00" and self.system_datetime <= '08:59':
                if data_time_status[8] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[8] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()

            elif self.system_datetime >= "09:00" and self.system_datetime <= '09:59':
                if data_time_status[9] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[9] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "10:00" and self.system_datetime <= '10:59':
                if data_time_status[10] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[10] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "11:00" and self.system_datetime <= '11:59':
                if data_time_status[11] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[11] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "12:00" and self.system_datetime <= '12:59':
                if data_time_status[12] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[12] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "13:00" and self.system_datetime <= '13:59':
                if data_time_status[13] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[13] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "14:00" and self.system_datetime <= '14:59':
                if data_time_status[14] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[14] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc() 
            elif self.system_datetime >= "15:00" and self.system_datetime <= '15:59':
                if data_time_status[15] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[15] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()   
            elif self.system_datetime >= "16:00" and self.system_datetime <= '16:59':
                if data_time_status[16] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[16] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "17:00" and self.system_datetime <= '17:59':
                if data_time_status[17] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[17] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "18:00" and self.system_datetime <= '18:59':
                if data_time_status[18] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[18] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "19:00" and self.system_datetime <= '19:59':
                if data_time_status[19] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[19] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "20:00" and self.system_datetime <= '20:59':
                if data_time_status[20] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[20] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "21:00" and self.system_datetime <= '21:59':
                if data_time_status[21] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[21] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "22:00" and self.system_datetime <= '22:59':
                if data_time_status[22] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[22] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
            elif self.system_datetime >= "23:00"   and self.system_datetime <= '23:59':
                if data_time_status[23] == "1":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                elif data_time_status[23] == "2":
                    if status_plc_out[0] == False:
                        mod.start_filtration()
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                    else :
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                        self.open_ozone_choc()
                else:
                    if status_plc_out[0] == True:
                        mod.stop_filtration() 
                        self.close_ozone_choc()
           
            else:
                if (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) <  float(data_setting[0]['setting_temperature']):
                    if status_plc_out[0] == False:
                        mod.stop_filtration() 
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
                    else:
                        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)

                else:
                    if status_plc_out[0] == True :
                        mod.stop_filtration()                             
          
        else :
            print("---------Close Filtration---------")
            if status_plc_out[0] == True:
              
                mod.stop_filtration()
            if status_plc_out[0] == False:
                if status_plc_out[1] == True:
                   
                    mod.stop_ozone_pump()

                if status_plc_out[1] == False:
                    mod.stop_chauffage()
                # if status_plc_out[2] == False:
                #     print("ปิด heater 2")
                #     mod.stop_chauffage2()


    def pompe_ozone_and_chauffage(self, status_plc_out, data_json, data_setting):
        print("-------------------pompe ozone and chauffage------------------")
        if status_plc_out[0] == True :

                #pompe zone
                if data_json[0]['sm_pomp_ozone'] != "0" :
                    if status_plc_out[1] == False :
                        mod.start_ozone_pump()
                else:
                    if status_plc_out[1] == True :
                        mod.stop_ozone_pump()

                #chauffage 
                if data_json[0]['sm_pomp_ozone'] == "0" :
                    if data_json[0]['sm_chauffage'] == "1":
                        if (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) <  float(data_setting[0]['setting_temperature']):
                            if status_plc_out[2] == False:
                                mod.start_chauffage()
                        elif (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) >=  float(data_setting[0]['setting_temperature']):
                            if status_plc_out[2] == True:
                                mod.stop_chauffage()
                    else:
                        if status_plc_out[2] == True:
                            mod.stop_chauffage()
                      

                elif data_json[0]['sm_pomp_ozone'] == "1" :
                    if data_json[0]['sm_chauffage'] == "1":
                     if status_plc_out[1] == True:
                        if (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) <  float(data_setting[0]['setting_temperature']):
                            if status_plc_out[2] == False:
                                mod.start_chauffage()
                        elif (float(self.temperature) - float(data_setting[0]['setting_temp_deff'])) >=  float(data_setting[0]['setting_temperature']):
                            if status_plc_out[2] == True:
                                mod.stop_chauffage()
                    else:
                        if status_plc_out[2] == True:
                            mod.stop_chauffage()
                            
    def open_ozone_choc(self):
        if self.status_relay[2] == False:
            modbus_relay.open_ozone_choc()
    def close_ozone_choc(self):
        if self.status_relay[2] == True:
            modbus_relay.close_ozone_choc()

    
