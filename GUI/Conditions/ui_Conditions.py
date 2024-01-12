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

import numpy as np

class formConditions(QMainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        #Initialise the Conditions form
        self.uiFormBakingConditions = Ui_windowBakingConditions()
        self.uiFormBakingConditions.setupUi(self)

        #Variable for the total number of jobs
        self.totalNumberJobs = 0
        #Initialise the array for the target temperatures
        #Assuming that the totoal numbers of targets <= 20
        self.arrayTargetTemperatures = np.zeros(20)
        self.currentClickedRow = 0 

        #Connect the add job button to the function
        self.uiFormBakingConditions.pushButton_addJob.clicked.connect(lambda: self.add_job())
        
        #Connect the delete job button to the function
        self.uiFormBakingConditions.pushButton_deleteJob.clicked.connect(lambda: self.delete_job())
        
        #Variable for the current clicked line edit
        self.selectedLineEdit = QLineEdit()
        #List for all line edits on the form
        self.listQLineEdit = [self.uiFormBakingConditions.lineEdit_T,
                              self.uiFormBakingConditions.lineEdit_Rate,
                              self.uiFormBakingConditions.lineEdit_Duration]
        #Install the event filter to all the line edits in the list
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].installEventFilter(self)
        
        #Set all the line edits read only and change the background colour
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].setReadOnly(True)
            self.listQLineEdit[i].setStyleSheet("QLineEdit"
                                                "{"
                                                "background: lightGray;"
                                                "}")
            
        #Connect the listWidget clicked to the function
        self.uiFormBakingConditions.listWidget_Jobs.itemClicked.connect(lambda: self.itemClicked())

        #Initialise the num pad
        self.form_numpad = formNumPad()
        #Connect the numpad signal to the function
        self.form_numpad.signalButton.connect(self.numpadInput)

    #Add a job to the list
    def add_job(self):
        self.uiFormBakingConditions.listWidget_Jobs.addItem(str(self.totalNumberJobs + 1))
        self.totalNumberJobs += 1
        
    
    #Delete the last job from the list
    def delete_job(self):
        self.uiFormBakingConditions.listWidget_Jobs.takeItem(self.totalNumberJobs - 1)
        self.totalNumberJobs -= 1
    
    #Enable the line edit when the item inside listWidget is clicked
    def itemClicked(self):
        #Set all the line edits read only and change the background colour
        for i in range(len(self.listQLineEdit)):
            self.listQLineEdit[i].setReadOnly(False)
            self.listQLineEdit[i].setStyleSheet("QLineEdit"
                                                "{"
                                                "background: white;"
                                                "}")
        self.currentClickedRow = self.uiFormBakingConditions.listWidget_Jobs.currentRow()

    #Event to show numpad form when the line edit is clicked
    def eventFilter(self, obj, event):   
        for i in range(len(self.listQLineEdit)):
            if obj == self.listQLineEdit[i]:
                if event.type() == event.MouseButtonPress:
                    self.showNumPad()
                    self.selectedLineEdit = obj
        
        return super(formConditions, self).eventFilter(obj, event)
    
    #Shown numpad
    def showNumPad(self):
        if self.form_numpad.isVisible() == True:
            self.form_numpad.close()

        self.form_numpad.show()
        #self.MainWindow_numpad.move(320,10)
    
    #Send the numpad button signal onto the clicked line edit
    @pyqtSlot(str)
    def numpadInput(self, sentString):
        originalText = self.selectedLineEdit.text()
        if sentString == "del":
            self.selectedLineEdit.setText(originalText[:-1])
        else:
            if sentString == "." and "." in originalText:
                pass
            else:
                self.selectedLineEdit.insert(sentString)
        
        if self.selectedLineEdit == self.listQLineEdit[0]:
            self.arrayTargetTemperatures[self.currentClickedRow] = (self.selectedLineEdit.text())

if __name__=="__main__":
    app = QApplication(sys.argv)
    widget = formConditions()
    widget.show()
    #widget.move(0,0)

    sys.exit(app.exec())