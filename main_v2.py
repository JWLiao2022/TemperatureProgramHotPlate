import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMainWindow
#Import different forms
from GUI.ToolsMenu.toolsMenu import Ui_FormToolsMenu

class Main(QMainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.uiFormToosMenu = Ui_FormToolsMenu()
        self.uiFormToosMenu.setupUi(self)        

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    #widget.move(0,0)

    sys.exit(app.exec())

