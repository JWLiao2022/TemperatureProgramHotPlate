import RPi.GPIO as GPIO
import os
import glob
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from time import time, sleep
from datetime import datetime

import numpy as np
from Control.ReportTemperature import clsTemperature

class clsStepMotor(QObject):
    ###Step resolution is 1/8 *4 (0.9^0), giving ~ 0.7572^0 per step 

    signalCurrentStatus = pyqtSignal(str)
    signalIsFinished = pyqtSignal()
    
    def __init__(self, userInputTemperature1, userInputTempRampRate1, userInputTempHoldTime1, 
                 userInputTemperature2, userInputTempRampRate2, userInputTempHoldTime2,
                 userInputTempReduceRate) -> None:
        super().__init__()
        self.Temperature1 = userInputTemperature1
        self.TempRampRate1 = userInputTempRampRate1
        self.TempHoldTime1 = userInputTempHoldTime1 * 60 #seconds
        self.Temperature2 = userInputTemperature2
        self.TempRampRate2 = userInputTempRampRate2
        self.TempHoldTime2 = userInputTempHoldTime2 * 60 #seconds
        self.TempReduceRate = userInputTempReduceRate
        self.readTemperature = clsTemperature()
        self.startTime = time()
        self.currentStepcount = 1
        self.continueRunning = False
        self.continueNextStage = False

        #Set up the GPIO
        self.TempResolution = 0.7572 #degree C/step at half resolution
        self.DIR = 20 ###GPIO pin 20
        self.STEP = 21 ###GPIO pin 21
        self.ENA = 23 ###GPIO pin 23
        self.RaiseT = 1 #clockwise
        self.ReduceT = 0 #counterclockwise
        self.securityStep = (150 - 25)/self.TempResolution
        self.securityStep = int(round(self.securityStep))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)

        self.MODE = (14, 15, 18)
        GPIO.setup(self.MODE, GPIO.OUT)
        self.RESOLUTION = {'Full': (0, 0, 0),
                    'Half': (1, 0, 0),
                    '1/4': (0, 1, 0),
                    '1/8': (1, 1, 0),
                    '1/16': (0, 0, 1),
                    '1/32': (1, 0, 1)}
        GPIO.output(self.MODE, self.RESOLUTION['1/8'])
    
    def startThermalCycle(self):
        #Heat from room temperature to T1.
        self.continueNextStage = True
        if self.continueNextStage:
            self.raiseTemperature(self.Temperature1, self.TempRampRate1, self.TempHoldTime1)
        #Heat from T1 to T2.
        if self.continueNextStage:
            self.raiseTemperature(self.Temperature2, self.TempRampRate2, self.TempHoldTime2)
        #Cool down.
        if self.continueNextStage:
            self.reduceTemperature(self.TempReduceRate)
            #Finish and clean the GPIO.
            print("Thermal cycle finished.\n")
            self.signalCurrentStatus.emit("{} Thermal cycle finished.\n".format(self.format_time()))
            GPIO.cleanup()
            #self.finished.emit()
            self.signalIsFinished.emit()
    
    def stopThermalCycle(self):
        #Finish and clean the GPIO.
        print("User stopped the thermal cycle.")
        self.signalCurrentStatus.emit("{} User stopped the thermal cycle.\n".format(self.format_time()))
        self.continueRunning = False
        self.continueNextStage = False
        GPIO.cleanup()
        #self.finished.emit()
        self.signalIsFinished.emit()    
    
    def raiseTemperature(self, targetTemperature, tempRampRate, tempHoldTime):
        #Heating
        #From room temperature to the targetTemperature
        print("Ramping the temperature to {:.2f} degree C".format(targetTemperature))
        self.signalCurrentStatus.emit("{} Ramping the temperature to {:.2f} \u00b0 C.\n".format(self.format_time(), targetTemperature))

        GPIO.output(self.DIR, self.RaiseT)
        delay = float(60/tempRampRate)
        currentTemp = self.readTemperature.cali_temp()
        #startTime = time()

        self.continueRunning = True

        while (self.continueRunning):
            print("current temperature is {:.2f} degree C at time of {:.2f} seconds...".format(currentTemp, time() - self.startTime))
            self.signalCurrentStatus.emit("{} Current temperature is {:.2f} \u00b0 C at time of {:.2f} minutes...\n".format(self.format_time(), currentTemp, (time() - self.startTime)/60))

            GPIO.output(self.ENA, GPIO.LOW)
            sleep(0.5)

            for x in range(4):
                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(0.02)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(0.02)

            GPIO.output(self.ENA, GPIO.HIGH)
            sleep(delay)

            currentTemp = self.readTemperature.cali_temp()
            self.currentStepcount += 1
            
            #Check if the heating continues
            if (currentTemp >= targetTemperature) and (self.currentStepcount < self.securityStep):
                self.continueRunning = False
        
        #Hold the temperature for the temperature hold time
        print("Holding at the first target temperature of {} degreeC. Real temperature is  {} degree C.".format(targetTemperature, currentTemp))
        self.signalCurrentStatus.emit("{} Holding at the temperature of {:.2f} \u00b0 C. Real temperature is {:.2f} \u00b0 C.\n".format(self.format_time(), currentTemp, targetTemperature))
        self.trusty_sleep(tempHoldTime)
    
    def reduceTemperature(self, tempReduceRate):
        print("Cooling down...")
        self.signalCurrentStatus.emit("{} Cooling down...\n".format(self.format_time()))
        step_count = self.currentStepcount
        current_step_count = 0
        GPIO.output(self.DIR, self.ReduceT)
        delay = tempReduceRate

        currentTemp = self.readTemperature.cali_temp()

        self.continueRunning = True
        
        while (self.continueRunning):
            print("current temperature is {} degree C at time of {} seconds...".format(currentTemp, time()-self.startTime))
            self.signalCurrentStatus.emit("{} Current temperature is {:.2f} \u00b0 C at time of {:.2f} minutes...\n".format(self.format_time(), currentTemp, (time() - self.startTime)/60))

            GPIO.output(self.ENA, GPIO.LOW)
            sleep(0.5)
            
            for y in range(4):
                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(0.02)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(0.02)

            GPIO.output(self.ENA, GPIO.HIGH)
            sleep(delay)
            currentTemp = self.readTemperature.cali_temp()
            current_step_count += 1

            #Check if the cooling process continues
            if (current_step_count >= step_count) or (currentTemp <= 30):
                self.continueRunning = False

    
    ######function to make sure the sleep function giving enough sleep time
    def trusty_sleep(self, n):
        start = time()
        while(time() - start < n):
            sleep(n - (time()-start))
    
    #Report current date and time
    def format_time(self):
        now = datetime.now()
        strNow = now.strftime('%d-%m-%Y %H:%M:%S.%f')

        return strNow[:-6]
