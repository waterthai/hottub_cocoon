import time
import sys
import datetime
from restart import *
from write_file import Write_file
from modbus_read import Modbus_read
from urllib.request import urlopen
import json
from close_all import Close_All


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


modbus_read = Modbus_read()
path_url = Path_url()
besgo = Main_Besgo()
close_all  = Close_All()
volt = Main_volt_tag()
heater  = Main_Heater()
main_pump = Main_HeatPump()
plc_mod = Modbus()
write_file = Write_file()

counter_pressure = 0
url_setting = path_url.url_setting
url_setting_mode = path_url.url_setting_mode
url_selection = path_url.url_selection

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
        print("xxxxxxxxxx"+str(plc_in[2]))
        # check nighttime swicth
        lock_machine = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
        if lock_machine.read() != "":
            sum_counter_lock = write_file.counter_locking(data_setting)
            
            if str(setting_mode[0]['sm_bypass']) == "1":
               write_file.set_zero_locking_counter()


        if plc_in[2] == False:
            if int(current_hour) < 21 and int(current_hour) > 7 : 
                print("in of time")
                #check bypass mode
                if str(setting_mode[0]['sm_bypass']) == "0":
                    count_down = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','r')
                    if count_down.read() == '':    
                        besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection)
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
                    besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection)
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
                    besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection)
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

                besgo.start_besgo(current_time, relay_8, plc, setting_mode, setting_selection)
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
except:
    restart_programs()

