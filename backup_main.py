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
from setting.path_url import Path_url
sys.path.append('/home/pi/hottub_ma/heater/')
from main_heater import Main_Heater


modbus_read = Modbus_read()
path_url = Path_url()
besgo = Main_Besgo()
close_all  = Close_All()
volt = Main_volt_tag()
heater  = Main_Heater()
plc_mod = Modbus()

counter_pressure = 0
url_setting = path_url.url_setting
url_setting_mode = path_url.url_setting_mode
url_selection = path_url.url_selection
besgo_status = False

try:
    while True:
        print("WORKING HOTTUB")
        system_time = datetime.datetime.now()
        current_time = system_time.strftime("%H:%M")
        current_hour =  system_time.strftime("%H")
        current_minute =  system_time.strftime("%M")
        sec_time =  system_time.strftime("%S")
        print("-------sec-----------"+str(sec_time))

        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())

        response_setting_mode =  urlopen(url_setting_mode)
        setting_mode = json.loads(response_setting_mode.read())

        response_selection =  urlopen(url_selection)
        setting_selection = json.loads(response_selection.read())

        read_pressure =  modbus_read.read_pressure()

        relay_8 = modbus_read.read_status_relay()
        print("relay"+str(relay_8))
        #read plc
        plc = modbus_read.read_status_plc_out()
        print("plc"+str(plc))
        #read temperature
        temperature = modbus_read.read_temperature()
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
        # #write file 
        write_file = Write_file(relay_8, plc, temperature, ph, orp, read_pressure)
        write_file.start_write()

        read_status_besgo = open('/home/pi/hottub_ma/txt_file/status_besgo.txt','r')
        status_bes = read_status_besgo.read().rstrip('\n')

        #check bypass mode
        if str(setting_mode[0]['sm_bypass']) == "0":
            if besgo_status == False:
                if float(data_setting[0]['setting_basse']) > float(read_pressure):
                    print("xxxxcounter_pressurexxxxx"+str(counter_pressure))   
                    besgo.start_besgo(current_time, relay_8, plc,setting_mode)
                    if status_bes == "True":
                        if relay_8[4] == True:
                             besgo_status = True
                        
                    else:
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8)
                        main_plc.start_plc()
                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()
                        counter_pressure = counter_pressure + 1
                        if int(counter_pressure) == int(data_setting[0]['setting_tentative']) :
                            minus_hour = int(current_hour) + int(data_setting[0]['setting_frequence'])
                            set_new_time = str(minus_hour)+':'+str(sec_time)
                            write_file = Write_file(relay_8, plc, temperature, ph, orp, read_pressure)
                            write_file.write_over_presssure(set_new_time)

                        elif int(counter_pressure) > int(data_setting[0]['setting_tentative']) :
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                            print("close all delay time")
                        elif int(counter_pressure) < int(data_setting[0]['setting_tentative']) :
                            if int(setting_mode[0]['sm_filtration']) != 0:
                                if plc[0] == False:
                                    plc_mod.start_filtration()
                    
                            
                    time.sleep(1)
                else:
                    count_down = open('./txt_file/count_down_close_system.txt','r')
                    if count_down.read() != '':
                        count_down_read = open('./txt_file/count_down_close_system.txt','w')
                        count_down_read.write('')
                        counter_pressure = 0
            
                    besgo.start_besgo(current_time, relay_8, plc, setting_mode)
                    heater.start_heater(temperature, plc, relay_8)
                    if relay_8[4] == True:
                        if besgo_status == False:
                            besgo_status = True
                    else:
                        if besgo_status == True:
                            besgo_status = False
                    print("---------besgo------status------"+str(besgo.status_working_besgo))
                    if status_bes == "False":
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8)
                        main_plc.start_plc()

                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()

                        main_ph = Main_PH(current_time, ph, orp, relay_8)
                        main_ph.start_ph()

                    time.sleep(1)
                    volt.start_volt(setting_selection)
                    
            else:
                count_down = open('./txt_file/count_down_close_system.txt','r')
                if count_down.read() != '':
                    count_down_read = open('./txt_file/count_down_close_system.txt','w')
                    count_down_read.write('')
                    counter_pressure = 0
        
                besgo.start_besgo(current_time, relay_8, plc,setting_mode)
                heater.start_heater(temperature, plc, relay_8)
                time.sleep(1)
                
            
        else:
            count_down = open('./txt_file/count_down_close_system.txt','r')
            if count_down.read() != '':
                count_down_read = open('./txt_file/count_down_close_system.txt','w')
                count_down_read.write('')
                counter_pressure = 0

            besgo.start_besgo(current_time, relay_8, plc)
            heater.start_heater(temperature, plc, relay_8)
 
            if relay_8[4] == True:
                if besgo_status == False:
                    besgo_status = True
            else:
                if besgo_status == True:
                    besgo_status = False
            print("---------besgo------status------"+str(besgo.status_working_besgo))
            if status_bes == "False":
                main_plc = Main_PLC(current_time, temperature, plc, relay_8)
                main_plc.start_plc()

                main_relay = Main_relay(relay_8, plc[0])
                main_relay.start_relay()

                main_ph = Main_PH(current_time, ph, orp, relay_8)
                main_ph.start_ph()
                
            time.sleep(1)
            volt.start_volt(setting_selection)
 

except:
    restart_programs()

