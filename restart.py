import os
import sys

def restart_programs():
    print("argv : ", sys.argv)
    print("sys executable : ", sys.executable)
    print("Restart Now")

    os.execv(sys.executable,['python'] + sys.argv)
