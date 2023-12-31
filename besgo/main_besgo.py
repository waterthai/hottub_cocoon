from urllib.request import urlopen
import json
import sys
from setting.path_url import Path_url
import datetime
from modbus_besgo import Modbus_besgo
sys.path.append('/home/pi/hottub_cocoon/plc/')
from modbus import Modbus
sys.path.append('/home/pi/hottub_cocoon/relay/')
from modbus_relay import Modbus_relay

path_url = Path_url()
url_besgo = path_url.url_besgo
url_besgo_setting= path_url.url_besgo_setting
mod_besgo = Modbus_besgo()
mod_plc = Modbus()
mod_relay = Modbus_relay()


class Main_Besgo():
    status_working_besgo = False
    counter_besgo_working = 0
    current_time = ''
    set_relay8 = ''
    set_plc_out = ''
    status_working = ""
    set_time_working = ''


    def start_besgo(self, current_time, set_relay8, set_plc_out, setting_mode, setting_selection,plc_all_in):
        if int(setting_selection[0]['backwash']) == 1:
            system_time = datetime.datetime.now()
            day = system_time.strftime("%a")
            besgo_response = urlopen(url_besgo)
            besgo_json = json.loads(besgo_response.read())
        
            besgo_settin_response = urlopen(url_besgo_setting)
            besgo_setting_json = json.loads(besgo_settin_response.read())
            #read array 8 chanel
            relay8 = set_relay8
            plc_read = set_plc_out
            print("--------Besgo-------"+str(besgo_setting_json[0]))
            if str(besgo_setting_json[0]['backwash_mode']) == "1":
                with open('/home/pi/txt_file/status_besgo.txt','w')  as write_status_besgo:
                    write_status_besgo.write("True")
                #ปิดการทำงาน อ่านค่า Sensor 
                with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                    write_loading_in_tank.write("True")
                #อ่านค่า counter เพื่อดับเครื่องทั้งหมดเพื่อให้เติมน้ำเข้าแท้ง
                with open("/home/pi/txt_file/counter_start_before_backwash.txt","r") as read_counter_before_backwash:
                    number_counter_before_backwash = read_counter_before_backwash.readline().strip()
                print("xxxxxxxxxxxxx backwash read : "+str(number_counter_before_backwash))
                if int(number_counter_before_backwash) <= (int(besgo_setting_json[0]['backwash_countdown']) * 60):
                    if plc_read[0] == True:
                        mod_plc.stop_filtration()
                        
                else:
                    #เปิดการทำงาน อ่านค่า Sensor ปกติ
                    with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                        write_loading_in_tank.write("False")
                    #ตั้งสถานะให้อ่าน counter backwash กำลังทำงานจาก Thread 
                    if plc_all_in[6] == True: 
                        if plc_all_in[7] == True:
                            if plc_read[0] == False:
                                    mod_plc.start_filtration()
                            if relay8[4] == False and plc_read[0] == True:
                                mod_besgo.open_besgo()
                                
                            if relay8[4] == True:
                                mod_besgo.close_all_working(relay8)
                    else:
                        if relay8[4] == True:
                            mod_besgo.close_besgo()

                
            elif str(besgo_setting_json[0]['backwash_mode']) == "2":
                print("backwash AUTO")
                with open('/home/pi/txt_file/status_besgo.txt','r') as read_status_besgo:
                    status_backwash = read_status_besgo.readline().strip()
                if status_backwash == "False":
                    for i in range(len(besgo_json)):
                        for j in range(len(besgo_json[i][0])):
                            if besgo_json[i][0][j] == day.upper():
                                time_split = besgo_json[i][1].split('-')  
                                print(time_split[0])         
                                print(time_split[1])               
                                if time_split[0] == current_time : 
                                    with open('/home/pi/txt_file/status_besgo.txt','w')  as write_status_besgo:
                                        write_status_besgo.write("True")
                            
                                    #ปิดการทำงาน อ่านค่า Sensor 
                                    with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                                        write_loading_in_tank.write("True")
                                       
                                #     if plc_read[0] == False:
                                #         mod_plc.start_filtration()
                                #     else:
                                #         if relay8[4] == False and plc_read[0] == True:
                                #             if self.status_working != "complete" or self.set_time_working != current_time:
                                #                 print("open bessgo working")
                                #                 mod_besgo.open_besgo()
                                #                 self.counter_besgo_working = self.counter_besgo_working + 1
                                #                 self.set_time_working = current_time
                                #                 write_status_besgo = open('/home/pi/txt_file/status_besgo.txt','w')
                                #                 write_status_besgo.write("True")
                                #                 self.status_working = "working"
                                    
                                # elif time_split[1] == current_time:    
                                #         print("ไม่ทำงาน besgo")
                                #         if relay8[4] == True:
                                #             mod_besgo.close_besgo()
                                #         write_status_besgo = open('/home/pi/txt_file/status_besgo.txt','w')
                                #         write_status_besgo.write("False")
                                #         self.counter_besgo_working = 0
                                #         self.status_working = ""
                else:
                    with open("/home/pi/txt_file/counter_start_before_backwash.txt","r") as read_counter_before_backwash:
                        number_counter_before_backwash = read_counter_before_backwash.readline().strip()
                    print("xxxxxxxxxxxxx backwash read : "+str(number_counter_before_backwash))
                    if int(number_counter_before_backwash) <= (int(besgo_setting_json[0]['backwash_countdown']) * 60):
                        if plc_read[0] == True:
                            mod_plc.stop_filtration()
                    else:
                        #เปิดการทำงาน อ่านค่า Sensor ปกติ
                        with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                            write_loading_in_tank.write("False")
                            
                        with open('/home/pi/txt_file/status_besgo_start_counter.txt','w') as status_besgo_start_counter:
                            status_besgo_start_counter.write("True")
                        with open('/home/pi/txt_file/counter_backwash_working.txt','r')  as read_counter_backwash:
                            number_counter_backwash = read_counter_backwash.readline().strip()
                        if int(number_counter_backwash) <= int(besgo_setting_json[0]['backwash_time']):
                        #ตั้งสถานะให้อ่าน counter backwash กำลังทำงานจาก Thread 
                            if plc_all_in[6] == True: 
                                if plc_all_in[7] == True:
                                    if plc_read[0] == False:
                                            mod_plc.start_filtration()
                                    if relay8[4] == False and plc_read[0] == True:
                                        mod_besgo.open_besgo()
                                        
                                    if relay8[4] == True:
                                        mod_besgo.close_all_working(relay8)
                            else:
                                if relay8[4] == True:
                                    mod_besgo.close_besgo()
                        else:
                            if relay8[4] == True:
                                mod_besgo.close_besgo()
                            with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                                write_status_besgo.write("False")
                               
                            with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter_in_tank:
                                write_counter_in_tank.write(str(0))
                                
                            with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                                write_counter.write(str(0))
                               
                            with open('/home/pi/txt_file/status_besgo_start_counter.txt','w')  as status_open_backwash:
                                    status_open_backwash.write("False")
                                    
                            with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                                    write_loading_in_tank.write("False")
                                   

                    
                                    
            else:
                if relay8[4] == True:
                    mod_besgo.close_besgo()
                if int(setting_mode[0]['sm_filtration']) == 0:
                    if relay8[4] == False:
                        mod_plc.stop_filtration()
                with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                    write_status_besgo.write("False")
                   
                with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter_in_tank:
                    write_counter_in_tank.write(str(0))
                    
                with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                    write_counter.write(str(0))
                   
                with open('/home/pi/txt_file/status_besgo_start_counter.txt','w')  as status_open_backwash:
                    status_open_backwash.write("False")
                        
                with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                    write_loading_in_tank.write("False")
                        
               
    

       