import RPi.GPIO as GPIO
import os
import glob
from time import time, sleep

#from PySide6.QtCore import QThread, Signal

import numpy as np

class clsTemperature():
    #signalCurrentTemperature = Signal(np.float32)
    #Set up the thermal sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    def __init__(self) -> None:
        super().__init__()
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        ####calibration factors, obtained by experiment
        self.a = 1.4839289
        self.b = -13.0432541
        ###end of calibration factors section
    
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)/1000.0

        return temp_c

    def cali_temp(self):
        readTemp = self.read_temp()
        caliTemp = self.a * readTemp + self.b

        return np.around(caliTemp, 1)