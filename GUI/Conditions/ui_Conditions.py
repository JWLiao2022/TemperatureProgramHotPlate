import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMainWindow
#Import different forms
from conditions import Ui_windowBakingConditions
#Import numpad form from a different dictory
sys.path.insert(1, 'C:/Users/Jung-WeiLiao/OneDrive - Durham Magneto Optics Ltd/Document/Qt/TemperatureProgramHotPlate/GUI/Numpad')
from ui_Numpadv2 import formNumPad

class formConditions(QMainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.uiFormBakingConditions = Ui_windowBakingConditions()
        self.uiFormBakingConditions.setupUi(self)
        
        self.selectedLineEdit = QLineEdit()
        self.listQLineEdit = [self.uiFormBakingConditions.lineEdit_T,
                              self.uiFormBakingConditions.lineEdit_Rate,
                              self.uiFormBakingConditions.lineEdit_Duration]
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].installEventFilter(self)

        self.form_numpad = formNumPad()
        self.form_numpad.signalButton.connect(self.numpadInput)
    
    def eventFilter(self, obj, event):   
        for i in range(len(self.listQLineEdit)):
            if obj == self.listQLineEdit[i]:
                if event.type() == event.MouseButtonPress:
                    self.showNumPad()
                    self.selectedLineEdit = obj
        
        return super(formConditions, self).eventFilter(obj, event)
    
    def showNumPad(self):
        if self.form_numpad.isVisible() == True:
            self.form_numpad.close()

        self.form_numpad.show()
        #self.MainWindow_numpad.move(320,10)
    
    @pyqtSlot(str)
    def numpadInput(self, sentString):
        if sentString == "del":
            self.selectedLineEdit.clear()
        else:
            self.selectedLineEdit.insert(sentString)

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = formConditions()
    widget.show()
    #widget.move(0,0)

    sys.exit(app.exec())