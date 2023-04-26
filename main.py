import sys
import os

#from PySide6.QtCore import QThread, Slot, QPoint, QTimer
#from PySide6.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit
from GUI.UI.ui_form import Ui_Widget
from GUI.Numpad.Numpad import Ui_Widget_Numpad
from Control.ReportTemperature import clsTemperature

import numpy as np
from datetime import datetime
import time

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
        #Set a timer for updating plot
        self.plotTimer = QTimer()
        self.plotTimer.timeout.connect(self.updatePlot)
        self.plotTimer.start(5000)
        self.now = datetime.now()
        #self.updateTimeStart = self.now.strftime("%H:%M:%S")

        self.plotAxisTime = []
        self.plotAxisTemperature = []

        #Create a list for all the QLineEdit
        self.listQLineEdit = [self.ui.lineEdit_T1, self.ui.lineEdit_Rate1, self.ui.lineEdit_Duration1, 
                         self.ui.lineEdit_T2, self.ui.lineEdit_Rate2, self.ui.lineEdit_Duration2,
                         self.ui.lineEdit_RateCool]

        #Connect the line edits to the numpad input signal
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].installEventFilter(self)  

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
    
    def updatePlot(self):
        datetime_end = datetime.now()
        print("Started at {}, now at {}".format(self.now, datetime_end))
        minutes_diff = (datetime_end - self.now).total_seconds()/60.0
        currentTemperature = self.readTemperature.cali_temp()
        self.plotAxisTime.append(minutes_diff)
        self.plotAxisTemperature.append(currentTemperature)
        self.ui.plotTemperatureVSTime.plot(self.plotAxisTime, self.plotAxisTemperature)
        

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

