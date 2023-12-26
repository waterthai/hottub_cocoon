from urllib.request import urlopen
import json
import sys
from setting.path_url import Path_url
import datetime
from modbus_besgo import Modbus_besgo
sys.path.append('/home/pi/hottub_ma/plc/')
from modbus import Modbus

path_url = Path_url()
url_besgo = path_url.url_besgo
url_besgo_setting= path_url.url_besgo_setting
mod_besgo = Modbus_besgo()
mod_plc = Modbus()


class Main_Besgo():
    status_working_besgo = False
    counter_besgo_working = 0
    current_time = ''
    set_relay8 = ''
    set_plc_out = ''
    status_working = ""
    set_time_working = ''


    def start_besgo(self, current_time, set_relay8, set_plc_out, setting_mode, setting_selection):
        if int(setting_selection[0]['backwash']) == 1:
            system_time = datetime.datetime.now()
            day = system_time.strftime("%a")
            besgo_response = urlopen(url_besgo)
            besgo_json = json.loads(besgo_response.read())
            print(besgo_json)
        
            besgo_settin_response = urlopen(url_besgo_setting)
            besgo_setting_json = json.loads(besgo_settin_response.read())
            #read array 8 chanel
            relay8 = set_relay8
            plc_read = set_plc_out
            print("--------Besgo-------"+str(besgo_setting_json[0]['backwash_mode']))
            if str(besgo_setting_json[0]['backwash_mode']) == "1":
                write_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','w')
                write_status_besgo.write("True")
                if plc_read[0] == False:
                    mod_plc.start_filtration()
                if relay8[4] == False and plc_read[0] == True:
                    mod_besgo.open_besgo()
                    
                if relay8[4] == True:
                    mod_besgo.close_all_working(relay8)
                
            elif str(besgo_setting_json[0]['backwash_mode']) == "2":
                print("backwash AUTO")
                for i in range(len(besgo_json)):
                    for j in range(len(besgo_json[i][0])):
                        print("xxxxxxxxxxxx"+besgo_json[i][0][j])
                        print("xxxxxxxxxxxx"+day.upper())
                        print("xxxxxxxxxxxx"+current_time)
                        if besgo_json[i][0][j] == day.upper():
                            time_split = besgo_json[i][1].split('-')  
                            print(time_split[0])         
                            print(time_split[1])               
                            if time_split[0] == current_time : 
                                if plc_read[0] == False:
                                    mod_plc.start_filtration()
                                else:
                                    if relay8[4] == False and plc_read[0] == True:
                                        if self.status_working != "complete" or self.set_time_working != current_time:
                                            print("open bessgo working")
                                            mod_besgo.open_besgo()
                                            self.counter_besgo_working = self.counter_besgo_working + 1
                                            self.set_time_working = current_time
                                            write_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','w')
                                            write_status_besgo.write("True")
                                            self.status_working = "working"
                                    # if relay8[4] == True:
                                    #     if int(besgo_setting_json[0]['backwash_time']) >= self.counter_besgo_working:
                                    #         self.counter_besgo_working =  self.counter_besgo_working + 1
                                    #     else:
                                    #         mod_besgo.close_besgo()
                                    #         self.counter_besgo_working = self.counter_besgo_working + 1
                                    #         write_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','w')
                                    #         write_status_besgo.write("False")
                                    #         self.status_working = 'complete'
                            elif time_split[1] == current_time:    
                                    print("ไม่ทำงาน besgo")
                                    if relay8[4] == True:
                                        mod_besgo.close_besgo()
                                    write_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','w')
                                    write_status_besgo.write("False")
                                    self.counter_besgo_working = 0
                                    self.status_working = ""
                                    
            else:
                if relay8[4] == True:
                    mod_besgo.close_besgo()
                if int(setting_mode[0]['sm_filtration']) == 0:
                    if relay8[4] == False:
                        mod_plc.stop_filtration()
                write_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','w')
                write_status_besgo.write("False")
    

       