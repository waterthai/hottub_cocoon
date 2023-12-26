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


sys.path.append('/home/pi/hottub_ma/besgo/')
from main_besgo import Main_Besgo
sys.path.append('/home/pi/hottub_ma/plc/')
from main_plc import Main_PLC
from modbus import Modbus
sys.path.append('/home/pi/hottub_ma/relay/')
from main_relay import Main_relay
sys.path.append('/home/pi/hottub_ma/ph/')
from main_ph import Main_PH
sys.path.append('/home/pi/hottub_ma/volttag/')
from main_volt_tag import Main_volt_tag
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_ma/heater/')
from main_heater import Main_Heater
from main_heatpump import Main_HeatPump
sys.path.append('/home/pi/hottub_ma/plc/')
sys.path.append('/home/pi/hottub_ma/relay/')
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
            read_status_backwash = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','r')
            status_backwash = read_status_backwash.read().rstrip('\n')
            if str(status_backwash) == "True":
                read_counter_backwash = open('/home/pi/hottub_ma/txt_file/counter_start_before_backwash.txt','r') 
                number_counter_backwash = read_counter_backwash.read().rstrip('\n')
                sum_counter = int(number_counter_backwash) + 1
                print("COUNTER BEFORE BACKWASH : "+str(sum_counter))
                with open('/home/pi/hottub_ma/txt_file/counter_start_before_backwash.txt','w') as write_counter:
                    write_counter.write(str(sum_counter))
                    write_counter.close()
            time.sleep(1)
        except:
            pass
               
        
def counter_start_backwash_time():
    while True:
        try:
            read_status_backwash = open('/home/pi/hottub_ma/txt_file/status_besgo_start_counter.txt','r')
            status_backwash = read_status_backwash.read().rstrip('\n')
            if str(status_backwash) == "True":
                read_counter_backwash = open('/home/pi/hottub_ma/txt_file/counter_backwash_working.txt','r') 
                number_counter_backwash = read_counter_backwash.read().rstrip('\n')
                sum_counter = int(number_counter_backwash) + 1
                print("COUNTER WORKING BACKWASH : "+str(sum_counter))
                with open('/home/pi/hottub_ma/txt_file/counter_backwash_working.txt','w') as write_counter:
                    write_counter.write(str(sum_counter))
                    write_counter.close()
            time.sleep(1)
        except:
            pass

        

before_backwash = threading.Thread(target=counter_before_backwash, args=())
before_backwash.start()
start_counter_backwash =  threading.Thread(target=counter_start_backwash_time, args=())
start_counter_backwash.start()

try:
    while True:
        print("WORKING HOTTUB")
        system_time = datetime.datetime.now()
        current_time = system_time.strftime("%H:%M")
        current_hour =  system_time.strftime("%H")
        current_minute =  system_time.strftime("%M")
        sec_time =  system_time.strftime("%S")
        print("-------sec-----------"+str(sec_time)+"----------"+str(current_hour))

        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())

        response_setting_mode =  urlopen(url_setting_mode)
        setting_mode = json.loads(response_setting_mode.read())

        response_selection =  urlopen(url_selection)
        setting_selection = json.loads(response_selection.read())


        read_pressure =  modbus_read.read_pressure(data_setting)
        print("pressure"+str(read_pressure))

        relay_8 = modbus_read.read_status_relay()
        print("relay"+str(relay_8))


        # #read plc
        plc = modbus_read.read_status_plc_out()
        print("plc"+str(plc))

        
        plc_in = modbus_read.read_status_plc_in()
        print("plc in"+str(plc_in))
        
        # #read temperature
        temperature = modbus_read.read_temperature(data_setting)
        print("temp"+str(temperature))
        # read ph
        ph = 0
        if int(setting_selection[0]['ph']) == 1:
            ph = modbus_read.read_ph()
        print("ph"+str(ph))
        #read orp
        orp = 0
        if int(setting_selection[0]['orp']) == 1:
            orp = modbus_read.read_orp()
        print("orp"+str(orp))
        #write file 
        heatpump = False
        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
            heatpump = modbus_read.read_heatpump()

        write_file.start_write(relay_8, plc, temperature, ph, orp, read_pressure, plc_in)

        read_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','r')
        status_bes = read_status_besgo.read().rstrip('\n')

        #อ่านค่า set pressure จาก front
        read_set_pressure = open('/home/pi/hottub_ma/txt_file/set_pressure.txt','r')
        set_pressure_text = read_set_pressure.read().rstrip('\n')
        split_set_pressure = set_pressure_text.split(",")

        # check nighttime swicth
        lock_machine = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
        if lock_machine.read() != "":
            sum_counter_lock = write_file.counter_locking(data_setting)
            
            if str(setting_mode[0]['sm_bypass']) == "1":
               write_file.set_zero_locking_counter()

        plc_all_in = modbus_read.read_all_plc_in()
        plc_all_out = modbus_read.read_all_plc_out()
        #ตรวจาอยลูกลอย
        read_loading_in_tank = open('/home/pi/hottub_ma/txt_file/stop_loading_in_tank.txt','r')
        status_loading_in_tank = read_loading_in_tank.read().rstrip('\n')

        if status_loading_in_tank == "False":
            if str(plc_all_in[6]) == "False" : 
                print("ปิด JA")
                if plc[0] == True:
                    plc_mod.stop_filtration()
            
            if str(plc_all_in[7]) =='False':
                print("เปิด โซลินอย")
                if plc_all_out[15] == False:
                    mod_relay.open_solenoid()
            else:
                print("เปิด JA")
                if plc[0] == False and setting_mode[0]['sm_filtration'] == 1: 
                    plc_mod.start_filtration()
            
            if plc_all_in[8] == True:
                print("ปิด โซลินอย"+str(plc_all_out[15]))
                if plc_all_out[15] == True:
                    mod_relay.close_solenoid()
        if str(plc_all_in[7]) == "True":
            if plc_in[2] == False:
                if int(current_hour) < 21 and int(current_hour) > 7 : 
                    print("in of time")
                    #check bypass mode
                    if str(setting_mode[0]['sm_bypass']) == "0":
                        count_down = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
                        if count_down.read() == '':    
                            besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                            if relay_8[4] == True:
                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                                else:
                                    heater.start_heater(temperature, plc, relay_8)
                            if status_bes == "False":
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8)
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
                                        print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)
                                        

                                    
                        else:
                            print("close Anoter Time")
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()

                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                            
                        
                    else:
                        count_down = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
                        if count_down.read() != '':
                            write_file.clear_pressure_time()
                            counter_pressure = 0
                        besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)

                        if status_bes == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8)
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
                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                else:
                    print("out of time")
                    close_all.start_close_plc(plc)
                    if plc[0] == False:
                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()
                    time.sleep(0.5)
            else:
                print("PLC NOT FALSE"+str(relay_8[4]))
                #check bypass mode
                if str(setting_mode[0]['sm_bypass']) == "0":
                    count_down = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
                    if count_down.read() == '':
                        besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)
                        
                        if status_bes == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8)
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
                                if float(split_set_pressure[0]) > float(read_pressure):
                                    counter_pressure = counter_pressure + 1
                                    print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                    if counter_pressure == int(split_set_pressure[1]) :
                                        minus_hour = int(current_hour) + int(split_set_pressure[2])
                                        set_new_time = str(minus_hour)+':'+str(sec_time)
                                        write_file.write_over_presssure(set_new_time)
                    else:
                        close_all.start_close_plc(plc)
                        if plc[0] == False:
                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
                            
                        
                else:
                    count_down = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
                    if count_down.read() != '':
                        write_file.clear_pressure_time()
                        counter_pressure = 0

                    besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection,plc_all_in)
                    if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump)
                            else:
                                heater.start_heater(temperature, plc, relay_8)
                    if status_bes == "False":
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8)
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
                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)

        else:
            # close_all.start_close_plc(plc)
            if plc[0] == False:
                main_relay = Main_relay(relay_8, plc[0])
                main_relay.start_relay()
except:
    restart_programs()

