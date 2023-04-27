import RPi.GPIO as GPIO
import os
import glob
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from time import time, sleep
from datetime import datetime

import numpy as np
from Control.ReportTemperature import clsTemperature

class clsStepMotor(QThread):
    ###Step resolution is 1/8 *4 (0.9^0), giving ~ 0.7572^0 per step 
    TempResolution = 0.7572 #degree C/step at half resolution
    DIR = 20 ###GPIO pin 20
    STEP = 21 ###GPIO pin 21
    ENA = 23 ###GPIO pin 23
    RaiseT = 1 #clockwise
    ReduceT = 0 #counterclockwise
    securityStep = (150 - 25)/TempResolution
    securityStep = int(round(securityStep))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

    MODE = (14, 15, 18)
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}
    GPIO.output(MODE, RESOLUTION['1/8'])

    signalCurrentStatus = pyqtSignal(str)
    signalCurrentStageFinished = pyqtSignal(int)
    signalTargetTReached = pyqtSignal()
    signalStartCoolingDown = pyqtSignal()
    
    def __init__(self, userInputTemperature1, userInputTempRampRate1, userInputTempHoldTime1, 
                 userInputTemperature2, userInputTempRampRate2, userInputTempHoldTime2,
                 userInputTempReduceRate) -> None:
        super().__init__()
        self.listTemperature = []
        self.listTempRampRate = []
        self.listTempHoldTime = []
        self.Temperature1 = userInputTemperature1
        self.TempRampRate1 = (60/userInputTempRampRate1) * 1000 #ms/step, each step ~ 1 ^0C temp change
        self.TempHoldTime1 = userInputTempHoldTime1 * 60 #seconds
        self.Temperature2 = userInputTemperature2
        self.TempRampRate2 = (60/userInputTempRampRate2) * 1000 #ms/step, each step ~ 1 ^0C temp change
        self.TempHoldTime2 = userInputTempHoldTime2 * 60 #seconds
        self.TempReduceRate = (60/userInputTempReduceRate) * 1000 #ms/step, 
        self.listTemperature.append(self.Temperature1)
        self.listTemperature.append(self.Temperature2)
        self.listTempRampRate.append(self.TempRampRate1)
        self.listTempRampRate.append(self.TempRampRate2)
        self.listTempHoldTime.append(self.TempHoldTime1)
        self.listTempHoldTime.append(self.TempHoldTime2)

        self.currentStage = 0
        self.currentTargetT = self.listTemperature[self.currentStage]
        self.currentTempRate = self.listTempRampRate[self.currentStage]
        self.currentTempHoldTime = self.listTempHoldTime[self.currentStage]

        self.totalNumStage = 2
        self.finalTemperature = 30

        self.readTemperature = clsTemperature()
        self.startTime = time()
        self.heatingStepcount = 0
        self.coolingStepcount = 0
        self.currentTemperature = self.readTemperature.cali_temp()
        #Initialising the timer
        self.timerRaisingT = QTimer()
        self.timerRaisingT.timeout.connect(self.stepperIncreasingTemperature)
        self.timerMonitoringRaisingT = QTimer()
        self.timerMonitoringRaisingT.timeout.connect(self.monitorRaisingTemperature)
        self.timerTargetTReached = QTimer()
        self.timerTargetTReached.timeout.connect(self.holdingTargetT)
        self.timerCoolingT = QTimer()
        self.timerCoolingT.timeout.connect(self.stepperReducingTemperature)
        self.timerMonitorCoolingT = QTimer()
        self.timerCoolingT.timeout.connect(self.monitorCoolingTemperature)
    
    def startThermalCycle(self):
        print("Ramping the temperature to {:.2f} degree C".format(self.currentTargetT))
        self.signalCurrentStatus.emit("{} Ramping the temperature to {:.2f} \u00b0 C.\n".format(self.format_time(), self.currentTargetT))
        self.timerRaisingT.start(self.currentTempRate)
        self.timerMonitoringRaisingT.start(self.currentTempRate/2)
    
    def stopThermalCycle(self):
        #Finish and clean the GPIO.
        print("User stopped the thermal cycle.")
        self.signalCurrentStatus.emit("{} User stopped the thermal cycle.\n".format(self.format_time()))
        #Stop all the timers
        if (self.timerRaisingT.isActive):
            self.timerRaisingT.stop()
        if (self.timerMonitoringRaisingT.isActive):
            self.timerMonitoringRaisingT.stop()
        if (self.timerTargetTReached.isActive):
            self.timerTargetTReached.stop()
        if (self.timerCoolingT.isActive):
            self.timerCoolingT.stop()
        if (self.timerMonitorCoolingT.isActive):
            self.timerMonitorCoolingT.stop()

        GPIO.cleanup()
        self.finished.emit()    
    
    def stepperIncreasingTemperature(self):
        GPIO.output(self.DIR, self.RaiseT)
        GPIO.output(self.ENA, GPIO.LOW)
        sleep(0.5)

        for x in range(4):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(0.02)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(0.02)

        GPIO.output(self.ENA, GPIO.HIGH)

        self.heatingStepcount += 1
    
    def stepperReducingTemperature(self):
        GPIO.output(self.DIR, self.ReduceT)
        GPIO.output(self.ENA, GPIO.LOW)
        sleep(0.5)
        
        for y in range(4):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(0.02)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(0.02)

        GPIO.output(self.ENA, GPIO.HIGH)

        self.coolingStepcount += 1
    
    def monitorRaisingTemperature(self):
        self.currentTemp = self.readTemperature.cali_temp()
        print("current temperature is {:.2f} degree C at time of {:.2f} seconds...".format(self.currentTemp, time() - self.startTime))
        self.signalCurrentStatus.emit("{} Current temperature is {:.2f} \u00b0 C...\n".format(self.format_time(), self.currentTemp)) 

        #Stop the time when reach the target temperature
        if self.currentTemp >= self.currentTargetT:
            print("Holding at the first target temperature of {} degreeC. Real temperature is  {} degree C.".format(self.currentTargetT, self.currentTemp))
            self.signalCurrentStatus.emit("{} Holding at the temperature of {:.2f} \u00b0 C. Real temperature is {:.2f} \u00b0 C.".format(self.format_time(), self.currentTemp, self.currentTargetT))
            self.signalTargetTReached.emit()
            self.timerRaisingT.stop()
            self.timerMonitoringT.stop()
            self.timerTargetTReached.start(self.currentTempHoldTime)
    
    def monitorCoolingTemperature(self):
        self.currentTemp = self.readTemperature.cali_temp()
        print("current temperature is {:.2f} degree C at time of {:.2f} seconds...".format(self.currentTemp, time() - self.startTime))
        self.signalCurrentStatus.emit("{} Current temperature is {:.2f} \u00b0 C...\n".format(self.format_time(), self.currentTemp)) 

        #End the process    
        if (self.currentTemp <= self.finalTemperature) or (self.coolingStepcount > self.heatingStepcount):
            print("Finished...")
            self.signalCurrentStatus.emit("{} Finished...\n".format(self.format_time()))
            self.timerCoolingT.stop()
            self.timerMonitorCoolingT.stop()
            GPIO.cleanup()
            self.finished.emit()  

    def holdingTargetT(self):
        #Feed in the new parameters
        self.currentStage += 1
        self.timerTargetTReached.stop()

        #Check if continue heating or start cooling
        if (self.currentStage < self.totalNumStage):
            #Start another heating step
            self.currentTargetT = self.listTemperature[self.currentStage]
            self.currentTempRate = self.listTempRampRate[self.currentStage]
            self.currentTempHoldTime = self.listTempHoldTime[self.currentStage]
            self.currentTemp = self.readTemperature.cali_temp()
            print("Ramping the temperature to {:.2f} degree C".format(self.currentTargetT))
            self.signalCurrentStatus.emit("{} Ramping the temperature to {:.2f} \u00b0 C.\n"
                                          .format(self.format_time(), self.currentTargetT))
            self.timerRaisingT.start(self.currentTempRate)
            self.timerMonitoringT.start(self.currentTempRate/2)
        elif (self.currentStage == self.totalNumStage):
            #Start cooling
            print("Cooling down...")
            self.signalCurrentStatus.emit("{} Cooling down...\n".format(self.format_time()))
            self.timerCoolingT.start(self.TempReduceRate)
            self.timerMonitorCoolingT.start(self.TempReduceRate/2)
    
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
