import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMainWindow
from Numpadv2 import Ui_MainWindow

class formNumPad(QMainWindow):
    signalButton = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiFormNumPad = Ui_MainWindow()
        self.uiFormNumPad.setupUi(self)
        self.uiFormNumPad.pushButton_0.clicked.connect(lambda: self.press_it("0"))
        self.uiFormNumPad.pushButton_1.clicked.connect(lambda: self.press_it("1"))
        self.uiFormNumPad.pushButton_2.clicked.connect(lambda: self.press_it("2"))
        self.uiFormNumPad.pushButton_3.clicked.connect(lambda: self.press_it("3"))
        self.uiFormNumPad.pushButton_4.clicked.connect(lambda: self.press_it("4"))
        self.uiFormNumPad.pushButton_5.clicked.connect(lambda: self.press_it("5"))
        self.uiFormNumPad.pushButton_6.clicked.connect(lambda: self.press_it("6"))
        self.uiFormNumPad.pushButton_7.clicked.connect(lambda: self.press_it("7"))
        self.uiFormNumPad.pushButton_8.clicked.connect(lambda: self.press_it("8"))
        self.uiFormNumPad.pushButton_9.clicked.connect(lambda: self.press_it("9"))
        self.uiFormNumPad.pushButton_del.clicked.connect(lambda: self.press_it("del"))
        self.uiFormNumPad.pushButton_dot.clicked.connect(lambda: self.press_it("."))
        
    @pyqtSlot(str)
    def press_it(self, sentString):
        self.signalButton.emit(sentString)