import time
import os
while True:
   
    myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
    with open(myFile, "r") as file:
        check_close = file.read().rstrip("\n")

    print(check_close)
    time.sleep(1)
