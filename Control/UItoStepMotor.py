import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from PyQt5.QtWidgets import QWidget
from Control.StepMotor import clsStepMotor

import threading

class clsUItoStepMotor(QObject):
    signalReceivedCurrentStatus = pyqtSignal(str)
    signalIsFinished = pyqtSignal()

    def __init__(self, userInputTemperature1, userInputTempRampRate1, userInputTempHoldTime1, 
                 userInputTemperature2, userInputTempRampRate2, userInputTempHoldTime2,
                 userInputTempReduceRate) -> None:
        super().__init__()
        self.Temperature1 = userInputTemperature1
        self.TempRampRate1 = userInputTempRampRate1
        self.TempHoldTime1 = userInputTempHoldTime1
        self.Temperature2 = userInputTemperature2
        self.TempRampRate2 = userInputTempRampRate2
        self.TempHoldTime2 = userInputTempHoldTime2
        self.TempReduceRate = userInputTempReduceRate
        self.thermalCycle = clsStepMotor(self.Temperature1, self.TempRampRate1, self.TempHoldTime1,
                                         self.Temperature2, self.TempRampRate2, self.TempHoldTime2,
                                         self.TempReduceRate)
        self.thread1 = myThread(self.thermalCycle)
        self.thermalCycle.signalCurrentStatus.connect(self.slot_reportCurrentStatus)
        self.thermalCycle.signalIsFinished.connect(self.slot_reportFinished)
        
        
    def startStepMotor(self):
        
        self.thread1.start()
    
    def stopStepMotor(self):
        self.thread1.stop()
        self.signalIsFinished.emit()
    
    #Report the current status (str) back to UI
    @pyqtSlot(str)
    def slot_reportCurrentStatus(self, txtCurrentStatusUpdate):
        self.signalReceivedCurrentStatus.emit(txtCurrentStatusUpdate)

    #Report when the process is finished
    @pyqtSlot()
    def slot_reportFinished(self):
        self.signalIsFinished.emit()

class myThread(threading.Thread):
    def __init__(self, inputObject):
        threading.Thread.__init__(self)
        self.runningObject = inputObject
        
    def run(self):
        self.runningObject.startThermalCycle()
    
    def stop(self):
        self.runningObject.stopThermalCycle()
