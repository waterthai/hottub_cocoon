import time
import sys
import datetime
from restart import *
from write_file import Write_file
from modbus_read import Modbus_read
from urllib.request import urlopen
import json
from close_all import Close_All
import threading


sys.path.append('/home/pi/hottub_cocoon/besgo/')
from main_besgo import Main_Besgo
sys.path.append('/home/pi/hottub_cocoon/plc/')
from main_plc import Main_PLC
from modbus import Modbus
sys.path.append('/home/pi/hottub_cocoon/relay/')
from main_relay import Main_relay
sys.path.append('/home/pi/hottub_cocoon/ph/')
from main_ph import Main_PH
sys.path.append('/home/pi/hottub_cocoon/volttag/')
from main_volt_tag import Main_volt_tag
sys.path.append('/home/pi/hottub_cocoon/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_cocoon/heater/')
from main_heater import Main_Heater
from main_heatpump import Main_HeatPump
sys.path.append('/home/pi/hottub_cocoon/plc/')
sys.path.append('/home/pi/hottub_cocoon/relay/')
from modbus_relay import Modbus_relay


modbus_read = Modbus_read()
path_url = Path_url()
besgo = Main_Besgo()
close_all  = Close_All()
volt = Main_volt_tag()
heater  = Main_Heater()
main_pump = Main_HeatPump()
plc_mod = Modbus()
write_file = Write_file()
mod_relay = Modbus_relay()

counter_pressure = 0
url_setting = path_url.url_setting
url_setting_mode = path_url.url_setting_mode
url_selection = path_url.url_selection


#เทรด นับเวลา หยุดปั้ม backwash
def counter_before_backwash():
    while True:
        try:
            with open('/home/pi/txt_file/status_besgo.txt','r') as read_status_backwash:
                status_backwash = read_status_backwash.readline().strip()
            if status_backwash == "True":
                with open('/home/pi/txt_file/counter_start_before_backwash.txt','r')  as read_counter_backwash:
                    number_counter_backwash = int(read_counter_backwash.readline().strip()) + 1
                with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter:
                    write_counter.write(str(number_counter_backwash))
            time.sleep(1)
        except:
            pass
               
def counter_start_backwash_time():
    while True:
        try:
            with open('/home/pi/txt_file/status_besgo_start_counter.txt','r') as read_status_backwash:
                status_backwash = read_status_backwash.readline().strip()
            if status_backwash == "True":
                with open('/home/pi/txt_file/counter_backwash_working.txt','r')  as read_counter_backwash:
                    number_counter_backwash = int(read_counter_backwash.readline().strip()) + 1
                with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                    write_counter.write(str(number_counter_backwash))   
            time.sleep(1)
        except:
            pass

def counter_start_heater():
    while True:
        try:
            with open('/home/pi/txt_file/status_working_heater.txt','r') as read_status_auto:
                status_working = read_status_auto.readline().strip()
            if status_working == "True":
                with open('/home/pi/txt_file/counter_open_heater.txt','r') as read_counter_open:
                    counter_open_heater = int(read_counter_open.readline().strip()) + 1
                if counter_open_heater <= 60:
                    with open('/home/pi/txt_file/counter_open_heater.txt','w') as write_counter_open:
                        write_counter_open.write(str(counter_open_heater))
            time.sleep(1)
        except:
            pass

        

before_backwash = threading.Thread(target=counter_before_backwash, args=())
before_backwash.start()
start_counter_backwash =  threading.Thread(target=counter_start_backwash_time, args=())
start_counter_backwash.start()
start_counter_heater =  threading.Thread(target=counter_start_heater, args=())
start_counter_heater.start()


while True:
    try:
        system_time = datetime.datetime.now()
        current_time = system_time.strftime("%H:%M")
        current_hour =  system_time.strftime("%H")
        current_minute =  system_time.strftime("%M")
        sec_time =  system_time.strftime("%S")

        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())

        response_setting_mode =  urlopen(url_setting_mode)
        setting_mode = json.loads(response_setting_mode.read())
        print(setting_mode)
        response_selection =  urlopen(url_selection)
        setting_selection = json.loads(response_selection.read())


        read_pressure =  modbus_read.read_pressure(data_setting)
      

        relay_8 = modbus_read.read_status_relay()
       


        # #read plc
        plc = modbus_read.read_status_plc_out()
       

        
        plc_in = modbus_read.read_status_plc_in()
       
        
        # #read temperature
        temperature = modbus_read.read_temperature(data_setting)
        
        # read ph
        ph = 0
        if int(setting_selection[0]['ph']) == 1:
            ph = modbus_read.read_ph()
     
        #read orp
        orp = 0
        if int(setting_selection[0]['orp']) == 1:
            orp = modbus_read.read_orp()
     
        #write file 
        heatpump = False
        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
            heatpump = modbus_read.read_heatpump()

        write_file.start_write(relay_8, plc, temperature, ph, orp, read_pressure, plc_in)

        read_status_besgo = open('/home/pi/txt_file/status_besgo.txt','r')
        status_bes = read_status_besgo.read().rstrip('\n')

        #อ่านค่า set pressure จาก front
        read_set_pressure = open('/home/pi/txt_file/set_pressure.txt','r')
        set_pressure_text = read_set_pressure.read().rstrip('\n')
        split_set_pressure = set_pressure_text.split(",")

        # check nighttime swicth
        # lock_machine = open('/home/pi/txt_file/count_down_close_system.txt','r')
        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
        with open(myFile, "r") as file:
            check_close = file.read().rstrip("\n")
        if check_close != "":
            sum_counter_lock = write_file.counter_locking(data_setting)
            
            if str(setting_mode[0]['sm_bypass']) == "1":
               write_file.set_zero_locking_counter()

        plc_all_in = modbus_read.read_all_plc_in()
        plc_all_out = modbus_read.read_all_plc_out()
        #ตรวจาอยลูกลอย
        read_loading_in_tank = open('/home/pi/txt_file/stop_loading_in_tank.txt','r')
        status_loading_in_tank = read_loading_in_tank.read().rstrip('\n')

        #ปุ่มกดปั้ม manual ถ้าไฟอิน ขากำหนด ทริก ไปตรวจสอบสถานะปั้ม ja ทำงานอยู่หรือไม่ ถ้าไม่ให้ส่งข้อมูลไปบันทึก mysql และส่ง data ขึ้น server เป็นโหมด manual
        

        if status_loading_in_tank == "False":
            if str(plc_all_in[6]) == "False" : 
               
                if plc[0] == True:
                    plc_mod.stop_filtration()
            
            if str(plc_all_in[7]) =='False':
              
                if plc_all_out[15] == False:
                    mod_relay.open_solenoid()
            else:
              
                if plc[0] == False and setting_mode[0]['sm_filtration'] == 1: 
                    plc_mod.start_filtration()
            
            if plc_all_in[8] == True:
             
                if plc_all_out[15] == True:
                    mod_relay.close_solenoid()

        if str(plc_all_in[7]) == "True":
            if plc_in[2] == False:
                if int(current_hour) < 21 and int(current_hour) > 7 : 

                    #check bypass mode
                    if str(setting_mode[0]['sm_bypass']) == "0":
                        print('no by pass')
                        # count_down = open('/home/pi/txt_file/count_down_close_system.txt','r')
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close == '':    
                            besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                            if relay_8[4] == True:
                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                                else:
                                    heater.start_heater(temperature, plc, relay_8)
                            if status_bes == "False":
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                                
                                main_ph = Main_PH(current_time, ph, orp, relay_8)
                                if plc[0] == True:
                                    main_ph.start_ph()

                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                                else:
                                    heater.start_heater(temperature, plc, relay_8)
                                #นับเวลาตรวจสอบ pressure ไม่มีแรงดัน
                                if plc[0] == True and relay_8[4] == False:
                                    if float(split_set_pressure[0]) > float(read_pressure):
                                        counter_pressure = counter_pressure + 1
                                        print("counter close filtration"+str(counter_pressure))
                                       
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)
                            else:
                                if status_loading_in_tank == "True":
                                    close_all.start_close_plc(plc)
                                    if plc[0] == False:
                                        main_relay = Main_relay(relay_8, plc[0])
                                        main_relay.start_relay()        

                                    
                        else:
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()

                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                            
                        
                    else:
                        # count_down = open('/home/pi/txt_file/count_down_close_system.txt','r')
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close != '':
                            write_file.clear_pressure_time()
                            counter_pressure = 0
                        besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)

                        if status_bes == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(current_time, ph, orp, relay_8)
                            if plc[0] == True:
                                main_ph.start_ph()

                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,plc_all_in)
                            else:
                                heater.start_heater(temperature, plc, relay_8)
                        else:
                            if status_loading_in_tank == "True":
                                close_all.start_close_plc(plc)
                                if plc[0] == False:
                                    main_relay = Main_relay(relay_8, plc[0])
                                    main_relay.start_relay()    
                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                else:     
                    close_all.start_close_plc(plc)
                    if plc[0] == False:
                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()
                    time.sleep(0.5)
            else:
                
                #check bypass mode
                if str(setting_mode[0]['sm_bypass']) == "0":
                    print('no by pass 2')
                   
                    myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                    with open(myFile, "r") as file:
                        check_close = file.read().rstrip("\n")
                    if check_close == "":
                        print('xxxxxx 1')
                        besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)
                        
                        if status_bes == "False":
                            print('xxxxxx 2')
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(current_time, ph, orp, relay_8)
                            if plc[0] == True:
                                main_ph.start_ph()
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)

                            if plc[0] == True and relay_8[4] == False:
                                print('xxxxxxxxx 3 : ')
                                print('xxxxxxxxx 4 : '+split_set_pressure[0])
                                print('xxxxxxxxx 4 : '+split_set_pressure[1])
                                print('xxxxxxxxx 5 : '+str(read_pressure))
                                if float(split_set_pressure[0]) > float(read_pressure):
                                    counter_pressure = counter_pressure + 1
                                    print('xxxxcounter close xxxxx : '+str(counter_pressure))
                                    if counter_pressure >= int(split_set_pressure[1]) :
                                        minus_hour = int(current_hour) + int(split_set_pressure[2])
                                        set_new_time = str(minus_hour)+':'+str(sec_time)
                                        write_file.write_over_presssure(set_new_time)
                        else:
                            if status_loading_in_tank == "True":
                                close_all.start_close_plc(plc)
                                if plc[0] == False:
                                    main_relay = Main_relay(relay_8, plc[0])
                                    main_relay.start_relay()    
                    else:
                        print('xxxxxx 2')
                        close_all.start_close_plc(plc)
                        if plc[0] == False:
                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
                            
                        
                else:
                    myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                    with open(myFile, "r") as file:
                        check_close = file.read().rstrip("\n")
                    # count_down = open('/home/pi/txt_file/count_down_close_system.txt','r')
                    if check_close != '':
                        write_file.clear_pressure_time()
                        counter_pressure = 0

                    besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                    if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)
                    if status_bes == "False":
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                        main_plc.start_plc()

                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()

                        main_ph = Main_PH(current_time, ph, orp, relay_8)
                        if plc[0] == True:
                            main_ph.start_ph()
                            
                        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                            main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                        else:
                            heater.start_heater(temperature, plc, relay_8)
                    else:
                        if status_loading_in_tank == "True":
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()    
                            
                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)

        else:
            # close_all.start_close_plc(plc)
            if plc[0] == False:
                main_relay = Main_relay(relay_8, plc[0])
                main_relay.start_relay()
    except:
        pass

