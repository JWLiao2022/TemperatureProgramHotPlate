# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1000, 550)
        font = QFont()
        font.setPointSize(18)
        Widget.setFont(font)
        self.gBoxCurrentTemperature = QGroupBox(Widget)
        self.gBoxCurrentTemperature.setObjectName(u"gBoxCurrentTemperature")
        self.gBoxCurrentTemperature.setGeometry(QRect(20, 10, 141, 81))
        self.gBoxCurrentTemperature.setFont(font)
        self.label_currentTemperature = QLabel(self.gBoxCurrentTemperature)
        self.label_currentTemperature.setObjectName(u"label_currentTemperature")
        self.label_currentTemperature.setGeometry(QRect(10, 40, 121, 41))
        self.gBoxUserInput = QGroupBox(Widget)
        self.gBoxUserInput.setObjectName(u"gBoxUserInput")
        self.gBoxUserInput.setGeometry(QRect(20, 90, 291, 451))
        self.gBoxUserInput.setFont(font)
        self.groupBox_3 = QGroupBox(self.gBoxUserInput)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(0, 370, 291, 81))
        self.layoutWidget = QWidget(self.groupBox_3)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(5, 41, 261, 42))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.lineEdit_RateCool = QLineEdit(self.layoutWidget)
        self.lineEdit_RateCool.setObjectName(u"lineEdit_RateCool")

        self.horizontalLayout_7.addWidget(self.lineEdit_RateCool)

        self.widget = QWidget(self.gBoxUserInput)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 30, 291, 341))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.layoutWidget1 = QWidget(self.groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 40, 271, 136))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit_T1 = QLineEdit(self.layoutWidget1)
        self.lineEdit_T1.setObjectName(u"lineEdit_T1")

        self.horizontalLayout.addWidget(self.lineEdit_T1)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_Rate1 = QLineEdit(self.layoutWidget1)
        self.lineEdit_Rate1.setObjectName(u"lineEdit_Rate1")

        self.horizontalLayout_2.addWidget(self.lineEdit_Rate1)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_Duration1 = QLineEdit(self.layoutWidget1)
        self.lineEdit_Duration1.setObjectName(u"lineEdit_Duration1")

        self.horizontalLayout_3.addWidget(self.lineEdit_Duration1)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.layoutWidget2 = QWidget(self.groupBox_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(0, 40, 261, 136))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_T2 = QLineEdit(self.layoutWidget2)
        self.lineEdit_T2.setObjectName(u"lineEdit_T2")

        self.horizontalLayout_4.addWidget(self.lineEdit_T2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.layoutWidget2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEdit_Rate2 = QLineEdit(self.layoutWidget2)
        self.lineEdit_Rate2.setObjectName(u"lineEdit_Rate2")

        self.horizontalLayout_5.addWidget(self.lineEdit_Rate2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.layoutWidget2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.lineEdit_Duration2 = QLineEdit(self.layoutWidget2)
        self.lineEdit_Duration2.setObjectName(u"lineEdit_Duration2")

        self.horizontalLayout_6.addWidget(self.lineEdit_Duration2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.gBoxTemperaturePlot = QGroupBox(Widget)
        self.gBoxTemperaturePlot.setObjectName(u"gBoxTemperaturePlot")
        self.gBoxTemperaturePlot.setGeometry(QRect(340, 10, 621, 521))
        self.plotTemperatureVSTime = PlotWidget(self.gBoxTemperaturePlot)
        self.plotTemperatureVSTime.setObjectName(u"plotTemperatureVSTime")
        self.plotTemperatureVSTime.setGeometry(QRect(20, 50, 591, 461))
        self.pushButton_Go = QPushButton(Widget)
        self.pushButton_Go.setObjectName(u"pushButton_Go")
        self.pushButton_Go.setGeometry(QRect(180, 10, 141, 81))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Temperature Programmer", None))
        self.gBoxCurrentTemperature.setTitle(QCoreApplication.translate("Widget", u"Current T", None))
        self.label_currentTemperature.setText(QCoreApplication.translate("Widget", u"Waiting...", None))
        self.gBoxUserInput.setTitle(QCoreApplication.translate("Widget", u"Temperature settings", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Cooling Stage", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Rate (<span style=\" vertical-align:super;\">0</span>C/min)</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Stage 1", None))
        self.label.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>T (<span style=\" vertical-align:super;\">0</span>C)</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Rate (<span style=\" vertical-align:super;\">0</span>C/min)</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Duration (mins)</p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Stage 2", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>T (<span style=\" vertical-align:super;\">0</span>C)</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Rate (<span style=\" vertical-align:super;\">0</span>C/min)</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Duration (mins)</p></body></html>", None))
        self.gBoxTemperaturePlot.setTitle(QCoreApplication.translate("Widget", u"Temperature variation with time", None))
        self.pushButton_Go.setText(QCoreApplication.translate("Widget", u"Go!", None))
    # retranslateUi

