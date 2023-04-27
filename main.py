import sys
import os

#from PySide6.QtCore import QThread, Slot, QPoint, QTimer
#from PySide6.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from GUI.UI.ui_form import Ui_Widget
from GUI.Numpad.Numpad import Ui_Widget_Numpad
from Control.ReportTemperature import clsTemperature
from Control.StepMotor import clsStepMotor

import numpy as np
from datetime import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

#Widget for the main window
class Widget(QWidget):
    def __init__(self, parent=None):
        #Initialise the main window
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        #Initialise the numpad
        self.widget_numpad = Widget_numpad()
        self.widget_numpad.signalButton.connect(self.numpadInput)
        self.selectedLineEdit = QLineEdit()
        #Initialise the real-time temperature reading
        self.readTemperature = clsTemperature()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCurrentTemperature)
        self.timer.start(1000)
        #Initialise the output plot
        self.initialisePlot()
        self.pen = pg.mkPen()
        #Set a timer for updating plot for every 30 seconds
        self.plotTimer = QTimer()
        self.plotTimer.timeout.connect(self.updatePlot)
        #self.plotTimer.start(30000)
        #self.now = datetime.now()
        #self.updateTimeStart = self.now.strftime("%H:%M:%S")
        #Disable the push button stop
        self.ui.pushButton_Stop.setEnabled(False)

        self.plotAxisTime = []
        self.plotAxisTemperature = []

        #Create a list for all the QLineEdit
        self.listQLineEdit = [self.ui.lineEdit_T1, self.ui.lineEdit_Rate1, self.ui.lineEdit_Duration1, 
                         self.ui.lineEdit_T2, self.ui.lineEdit_Rate2, self.ui.lineEdit_Duration2,
                         self.ui.lineEdit_RateCool]

        #Connect the line edits to the numpad input signal
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].installEventFilter(self)  
        
        #Start thermal cycle
        self.ui.pushButton_Go.clicked.connect(self.startThermalCycle)

        #Stop thermal cycle
        self.ui.pushButton_Stop.clicked.connect(self.stopThermalCycle)

    def updateCurrentTemperature(self):
        currentTemperature = self.readTemperature.cali_temp()
        self.ui.label_currentTemperature.setText("{} \u00b0 C".format(currentTemperature))
    
    def mousePressEvent(self, event):
        print("Main Widget Mouse Press")
        #Close the numpad
        if self.widget_numpad.isVisible() == True:
            self.widget_numpad.close()

        super(Widget, self).mousePressEvent(event)
    
    def eventFilter(self, obj, event):
        if self.ui.pushButton_Go.isEnabled():    
            for i in range(len(self.listQLineEdit)):
                if obj == self.listQLineEdit[i]:
                    if event.type() == event.MouseButtonPress:
                        print("Widget click", obj)
                        self.showingFromNumPad()
                        self.selectedLineEdit = obj
        
        return super(Widget, self).eventFilter(obj, event)

    def showingFromNumPad(self):
        if self.widget_numpad.isVisible() == True:
            self.widget_numpad.close()
        self.widget_numpad.show()

    @pyqtSlot(str)
    def numpadInput(self, sentString):
        if sentString == "Clear":
            self.selectedLineEdit.clear()
        else:
            self.selectedLineEdit.insert(sentString)
    
    def initialisePlot(self):
        self.ui.plotTemperatureVSTime.setLabel(axis='left', text='Temperature (\u00b0 C)')
        self.ui.plotTemperatureVSTime.setLabel(axis='bottom', text='Time (min)')
        self.ui.plotTemperatureVSTime.showAxis('right')
        self.ui.plotTemperatureVSTime.showAxis('top')
        self.pen = pg.mkPen(color=(255, 0, 0))
        font = QtGui.QFont()
        font.setPixelSize(40)
        self.ui.plotTemperatureVSTime.getAxis('bottom').tickFont = font
        self.ui.plotTemperatureVSTime.getAxis('bottom').setStyle(tickTextOffset=20)
        self.ui.plotTemperatureVSTime.getAxis('left').tickFont=font
        self.ui.plotTemperatureVSTime.getAxis('left').setStyle(tickTextOffset=20)
    
    def updatePlot(self):
        datetime_end = datetime.now()
        minutes_diff = (datetime_end - self.now).total_seconds()/60.0
        currentTemperature = self.readTemperature.cali_temp()
        #currentTemperature = 21
        self.plotAxisTime.append(minutes_diff)
        self.plotAxisTemperature.append(currentTemperature)
        self.ui.plotTemperatureVSTime.plot(self.plotAxisTime, self.plotAxisTemperature, pen = (255, 255, 0), symbol='s', symbolSize = 10, symbolBrush=(255, 255, 0),
                                           symbolPen=(255, 255, 0))
    
    def startThermalCycle(self):
        #Input the user input parameters
        targetTemperature1 = float(self.ui.lineEdit_T1.text())
        targetTempRampRate1 = float(self.ui.lineEdit_Rate1.text())
        targetTempHoldTime1 = float(self.ui.lineEdit_Duration1.text())
        targetTemperature2 = float(self.ui.lineEdit_T2.text())
        targetTempRampRate2 = float(self.ui.lineEdit_Rate2.text())
        targetTempHoldTime2 = float(self.ui.lineEdit_Duration2.text())
        targetTempCoolRate = float(self.ui.lineEdit_RateCool.text())
        
        self.thermalCycle = clsStepMotor(targetTemperature1, targetTempRampRate1, targetTempHoldTime1, 
                                         targetTemperature2, targetTempRampRate2, targetTempHoldTime2, 
                                         targetTempCoolRate)
        self.thread = QThread()
        self.thermalCycle.moveToThread(self.thread)
        self.thread.started.connect(self.thermalCycle.startThermalCycle)
        self.thermalCycle.finished.connect(self.thread.quit)
        self.thermalCycle.finished.connect(self.thermalCycle.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()

        self.thermalCycle.signalCurrentStatus.connect(self.slot_updateCurrentStatus)

        self.ui.pushButton_Go.setEnabled(False)
        self.ui.pushButton_Go.setText("Under baking...")
        self.ui.pushButton_Stop.setEnabled(True)

        #Set all the line edits read only and change the background colour
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].setReadOnly(True)
            self.listQLineEdit[i].setStyleSheet("QLineEdit"
                                                "{"
                                                "background: lightGray;"
                                                "}")
        
        #Close the numpad window
        if self.widget_numpad.isVisible() == True:
            self.widget_numpad.close()
        
        self.thread.finished.connect(self.slot_resetGoBotton)

        #Start update the plot at every 30 seconds
        #Reset the input plot lists before starting 
        self.plotAxisTime = [0]
        self.plotAxisTemperature = [self.readTemperature.cali_temp()]
        self.plotTimer.start(30000)
        self.now = datetime.now()
    
    def stopThermalCycle(self):
        self.thermalCycle.stopThermalCycle()
        self.thermalCycle.finished.connect(self.thread.quit)
        self.thermalCycle.finished.connect(self.thermalCycle.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.slot_resetGoBotton)
    
    #Update the current status
    @pyqtSlot(str)
    def slot_updateCurrentStatus(self, txtStatusUpdate):
        self.ui.textEditCurrentStatus.insertPlainText(txtStatusUpdate)
        #Anchor the vertical scroll bar to the bottom.
        vsb = self.ui.textEditCurrentStatus.verticalScrollBar()
        vsb.setValue(vsb.maximum())
    
    #Reset the Go push button when the thermal cycle has finished.
    @pyqtSlot()
    def slot_resetGoBotton(self):
        self.ui.pushButton_Go.setEnabled(True)
        self.ui.pushButton_Go.setText("Go!")
        self.ui.pushButton_Stop.setEnabled(False)

        #Set all the line edits editable and change the backbround colour back
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].setReadOnly(False)
            self.listQLineEdit[i].setStyleSheet("QLineEdit"
                                                "{"
                                                "background: white;"
                                                "}")
        
        #Stop updating the plot
        self.plotTimer.stop()

#Widget for the numpad
class Widget_numpad(QWidget):
    signalButton = pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()
        self.ui_numpad = Ui_Widget_Numpad()
        self.ui_numpad.setupUi(self)
        self.ui_numpad.pushButton_0.clicked.connect(self.button_0_clicked)
        self.ui_numpad.pushButton_1.clicked.connect(self.button_1_clicked)
        self.ui_numpad.pushButton_2.clicked.connect(self.button_2_clicked)
        self.ui_numpad.pushButton_3.clicked.connect(self.button_3_clicked)
        self.ui_numpad.pushButton_4.clicked.connect(self.button_4_clicked)
        self.ui_numpad.pushButton_5.clicked.connect(self.button_5_clicked)
        self.ui_numpad.pushButton_6.clicked.connect(self.button_6_clicked)
        self.ui_numpad.pushButton_7.clicked.connect(self.button_7_clicked)
        self.ui_numpad.pushButton_8.clicked.connect(self.button_8_clicked)
        self.ui_numpad.pushButton_9.clicked.connect(self.button_9_clicked)
        self.ui_numpad.pushButton_Dot.clicked.connect(self.button_dot_clicked)
        self.ui_numpad.pushButton_Clear.clicked.connect(self.button_clear_clicked)
        
    def button_0_clicked(self):
        self.signalButton.emit("0")

    def button_1_clicked(self):
        self.signalButton.emit("1")
    
    def button_2_clicked(self):
        self.signalButton.emit("2")
    
    def button_3_clicked(self):
        self.signalButton.emit("3")
    
    def button_4_clicked(self):
        self.signalButton.emit("4")
    
    def button_5_clicked(self):
        self.signalButton.emit("5")
    
    def button_6_clicked(self):
        self.signalButton.emit("6")
    
    def button_7_clicked(self):
        self.signalButton.emit("7")
    
    def button_8_clicked(self):
        self.signalButton.emit("8")
    
    def button_9_clicked(self):
        self.signalButton.emit("9")
    
    def button_dot_clicked(self):
        self.signalButton.emit(".")
    
    def button_clear_clicked(self):
        self.signalButton.emit("Clear")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())

