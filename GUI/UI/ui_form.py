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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QSizePolicy,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.gBoxCurrentTemperature = QGroupBox(Widget)
        self.gBoxCurrentTemperature.setObjectName(u"gBoxCurrentTemperature")
        self.gBoxCurrentTemperature.setGeometry(QRect(20, 30, 331, 101))
        font = QFont()
        font.setPointSize(20)
        self.gBoxCurrentTemperature.setFont(font)
        self.label_currentTemperature = QLabel(self.gBoxCurrentTemperature)
        self.label_currentTemperature.setObjectName(u"label_currentTemperature")
        self.label_currentTemperature.setGeometry(QRect(20, 50, 301, 41))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.gBoxCurrentTemperature.setTitle(QCoreApplication.translate("Widget", u"Current temperature", None))
        self.label_currentTemperature.setText(QCoreApplication.translate("Widget", u"Waiting for the reading...", None))
    # retranslateUi

