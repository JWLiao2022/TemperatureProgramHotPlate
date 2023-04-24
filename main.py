import sys
import os

#from PySide6.QtCore import QThread, Slot, QPoint, QTimer
#from PySide6.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget
from GUI.UI.ui_form import Ui_Widget
from GUI.Numpad.Numpad import Ui_Widget_Numpad
from Control.ReportTemperature import clsTemperature

import numpy as np

#Widget for the main window
class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.readTemperature = clsTemperature()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCurrentTemperature)
        self.timer.start(1000)

        self.ui.lineEdit_T1.installEventFilter(self)
    
    def updateCurrentTemperature(self):
        currentTemperature = self.readTemperature.cali_temp()
        self.ui.label_currentTemperature.setText("{} \u00b0 C".format(currentTemperature))
    
    def mousePressEvent(self, event):
        print("Main Widget Mouse Press")
        super(Widget, self).mousePressEvent(event)
    
    def eventFilter(self, obj, event):
        if obj == self.ui.lineEdit_T1:
            if event.type() == event.MouseButtonPress:
                print("Widget click", obj)
                self.showingFromNumPad()
        
        return super(Widget, self).eventFilter(obj, event)

    def showingFromNumPad(self):
        widget_numpad = Widget_numpad()
        widget_numpad.show()
        widget_numpad.ui_numpad.gridLayout.buttonClicked.connect(self.numpadInput)

    def numpadInput(self, button):
        char = str(button.text())

        self.ui.lineEdit_T1.insert(char)

#Widget for the numpad
class Widget_numpad(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui_numpad = Ui_Widget_Numpad()
        self.ui_numpad.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())

