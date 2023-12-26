from modbus_volt import  Modbus_Volt
modbus_volt = Modbus_Volt()

class Main_volt_tag():
    def start_volt(self, setting_selection):
        if int(setting_selection[0]['volt_1_ph']) == 1 or int(setting_selection[0]['volt_2_ph']) == 1:
            read_volt = modbus_volt.read_volt()
            print("-----------------VOLT-------------"+str(read_volt))
            string_volt = str(read_volt[0])
            len_string = len(string_volt)
            len_decimal = len_string - 1
            string_integer = string_volt[0:len_decimal]
            string_dec = string_volt[len_decimal : len_string]
            volt_set = string_integer+'.'+string_dec

            string_volt1 = str(read_volt[1])
            len_string1 = len(string_volt1)
            len_decimal1 = len_string1 - 1
            string_integer1 = string_volt1[0:len_decimal1]
            string_dec1 = string_volt1[len_decimal1 : len_string1]
            volt_set1 = string_integer1+'.'+string_dec1

            string_volt2 = str(read_volt[2])
            len_string2 = len(string_volt2)
            len_decimal2 = len_string2 - 1
            string_integer2 = string_volt2[0:len_decimal2]
            string_dec2 = string_volt2[len_decimal2 : len_string2]
            volt_set2 = string_integer2+'.'+string_dec2

            txt_set = volt_set+","+volt_set1+","+volt_set2
            # txt_set = "0,0,0"

            open_volt = open("/home/pi/hottub_ma/txt_file/volt_tag.txt","w")
            open_volt.write(str(txt_set))
        else:
            txt_set = "0,0,0"
            open_volt = open("/home/pi/hottub_ma/txt_file/volt_tag.txt","w")
            open_volt.write(str(txt_set))




