import sys
import os

#from PySide6.QtCore import QThread, Slot, QPoint, QTimer
#from PySide6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget
from GUI.UI.ui_form import Ui_Widget
from Control.ReportTemperature import clsTemperature

import numpy as np

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.readTemperature = clsTemperature()
        self.timer = QTimer()
        self.time.timeout.connect(self.updateCurrentTemperature)
        self.time.start(1000)
    
    def updateCurrentTemperature(self):
        currentTemperature = self.readTemperature.cali_temp()
        self.ui.label_currentTemperature.setText("{} \u00b0 C".format(currentTemperature))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())

