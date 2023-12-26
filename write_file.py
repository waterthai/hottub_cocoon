
import time
class Write_file():


    def start_write(self, relay_8, plc_status, temperature, ph, orp, pressure, plc_in):
        print("writefile open")
        relay_file = open('/home/pi/hottub_ma/txt_file/status_relay_8.txt','w')
        relay_file.write(str(relay_8))

        plc_file = open('/home/pi/hottub_ma/txt_file/status_plc.txt','w')
        plc_file.write(str(plc_status))

        plc_file_in = open('/home/pi/hottub_ma/txt_file/status_plc_in.txt','w')
        plc_file_in.write(str(plc_in))

        temperature_file = open('/home/pi/hottub_ma/txt_file/temperature.txt','w')
        temperature_file.write(str(temperature))


        ph_file = open('/home/pi/hottub_ma/txt_file/ph.txt','w')
        ph_file.write(str(ph))
        
        orp_file = open('/home/pi/hottub_ma/txt_file/orp.txt','w')
        orp_file.write(str(orp))

        pressure_file = open('/home/pi/hottub_ma/txt_file/pressure.txt','w')
        pressure_file.write(str(pressure))
        print("writefile close")

    def write_over_presssure(self,pressure):
        print("writefile pressure open")
        pressure_file = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','w')
        pressure_file.write(str(pressure))
        print("writefile pressure close")

    def clear_pressure_time(self):
        count_down_read = open('/home/pi/hottub_ma/txt_file/count_down_close_system.txt','w')
        count_down_read.write('')

    def counter_locking(self, data_setting):
        try:
            read_counter_lock = open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt','r')
            if read_counter_lock.read() != "":
                counter_lock_machine = int(read_counter_lock.read())
                sum_counter_lock = counter_lock_machine + 1
                print("-----xxx---"+str(sum_counter_lock))
                with open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt', 'w') as write_lock_machine:
                    write_lock_machine.write(str(sum_counter_lock))
                # write_lock_machine = open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt','w')
                # write_lock_machine.write(str(sum_counter_lock))
                if sum_counter_lock >= ((int(data_setting[0]['setting_frequence']) * 60) * 60):
                        self.clear_pressure_time()
                        time.sleep(0.5)
                        # write_lock_machine = open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt','w')
                        # write_lock_machine.write("0")
                        with open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt', 'w') as f:
                            f.write("0")
            else:
                with open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt', 'w') as f:
                    f.write("0")
        except:
             pass
    def set_zero_locking_counter(self):
        self.clear_pressure_time()
        time.sleep(0.5)
        with open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt', 'w') as f:
             f.write("0")
        # write_lock_machine = open('/home/pi/hottub_ma/txt_file/couter_lock_machine.txt','w')
        # write_lock_machine.write("0")


