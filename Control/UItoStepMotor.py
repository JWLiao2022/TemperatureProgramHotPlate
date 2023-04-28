import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject
from Control.StepMotor import clsStepMotor

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
        
    
    def startStepMotor(self):
        self.thread = QThread()
        self.thermalCycle = clsStepMotor(self.Temperature1, self.TempRampRate1, self.TempHoldTime1,
                                         self.Temperature2, self.TempRampRate2, self.TempHoldTime2,
                                         self.TempReduceRate)
        self.thermalCycle.moveToThread(self.thread)
        self.thread.started.connect(self.thermalCycle.startThermalCycle)
        #Connect signals from the working thread to the main thread
        self.thermalCycle.finished.connect(self.thread.quit)
        self.thermalCycle.finished.connect(self.thermalCycle.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #Report when the thread is finished
        self.thread.finished.connect(self.slot_reportFinished)
        #Pass the reported current status to the following function
        self.thermalCycle.signalCurrentStatus.connect(self.slot_reportCurrentStatus)

        self.thread.start()
    
    def stopStepMotor(self):
        self.thermalCycle.stopThermalCycle()
        self.thermalCycle.finished.connect(self.thread.quit)
        self.thermalCycle.finished.connect(self.thermalCycle.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #Report when the thread is finished
        self.thread.finished.connect(self.slot_reportFinished)
    
    #Report the current status (str) back to UI
    @pyqtSlot(str)
    def slot_reportCurrentStatus(self, txtCurrentStatusUpdate):
        self.signalReceivedCurrentStatus.emit(txtCurrentStatusUpdate)

    #Report when the process is finished
    @pyqtSlot()
    def slot_reportFinished(self):
        self.signalIsFinished.emit()