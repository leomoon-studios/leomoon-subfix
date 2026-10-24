# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(451, 351)
        main.setMinimumSize(QSize(451, 351))
        icon = QIcon()
        icon.addFile(u":/res/icons/main.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main.setWindowIcon(icon)
        main.setStyleSheet(u"QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}\n"
"QLabel#titleLbl {color: rgb(68,68,68);}\n"
"QLabel#verLbl {color: rgb(68,68,68);}")
        self.centralwidget = QWidget(main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.banner = QFrame(self.centralwidget)
        self.banner.setObjectName(u"banner")
        self.banner.setMinimumSize(QSize(0, 81))
        self.banner.setMaximumSize(QSize(16777215, 81))
        self.banner.setLayoutDirection(Qt.LeftToRight)
        self.banner.setFrameShape(QFrame.NoFrame)
        self.banner.setFrameShadow(QFrame.Raised)
        self.banner.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.banner)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(11, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.logoLbl = QLabel(self.banner)
        self.logoLbl.setObjectName(u"logoLbl")
        self.logoLbl.setMinimumSize(QSize(61, 61))
        self.logoLbl.setMaximumSize(QSize(61, 61))
        self.logoLbl.setPixmap(QPixmap(u":/res/icons/main.png"))
        self.logoLbl.setScaledContents(True)

        self.horizontalLayout.addWidget(self.logoLbl)

        self.horizontalSpacer_2 = QSpacerItem(11, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.titleFrm = QFrame(self.banner)
        self.titleFrm.setObjectName(u"titleFrm")
        self.titleFrm.setFrameShape(QFrame.NoFrame)
        self.titleFrm.setFrameShadow(QFrame.Raised)
        self.titleFrm.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.titleFrm)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.titleLbl = QLabel(self.titleFrm)
        self.titleLbl.setObjectName(u"titleLbl")
        self.titleLbl.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setFamilies([u"Vazir"])
        font.setPointSize(15)
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.titleLbl.setFont(font)

        self.verticalLayout_2.addWidget(self.titleLbl)

        self.verLbl = QLabel(self.titleFrm)
        self.verLbl.setObjectName(u"verLbl")
        font1 = QFont()
        font1.setFamilies([u"Vazir"])
        font1.setPointSize(10)
        self.verLbl.setFont(font1)

        self.verticalLayout_2.addWidget(self.verLbl)

        self.verticalSpacer_2 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.titleFrm)


        self.verticalLayout.addWidget(self.banner)

        self.contentFrm = QFrame(self.centralwidget)
        self.contentFrm.setObjectName(u"contentFrm")
        self.contentFrm.setFrameShape(QFrame.NoFrame)
        self.contentFrm.setFrameShadow(QFrame.Raised)
        self.contentFrm.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.contentFrm)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.dropLbl = QLabel(self.contentFrm)
        self.dropLbl.setObjectName(u"dropLbl")
        font2 = QFont()
        font2.setFamilies([u"Vazir"])
        font2.setPointSize(30)
        font2.setBold(True)
        font2.setItalic(False)
        self.dropLbl.setFont(font2)
        self.dropLbl.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.dropLbl)

        self.fixCbox = QCheckBox(self.contentFrm)
        self.fixCbox.setObjectName(u"fixCbox")
        self.fixCbox.setFont(font1)
        self.fixCbox.setChecked(True)

        self.verticalLayout_3.addWidget(self.fixCbox)


        self.verticalLayout.addWidget(self.contentFrm)

        self.statusFrm = QFrame(self.centralwidget)
        self.statusFrm.setObjectName(u"statusFrm")
        self.statusFrm.setMinimumSize(QSize(0, 31))
        self.statusFrm.setMaximumSize(QSize(16777215, 31))
        self.statusFrm.setFont(font1)
        self.statusFrm.setFrameShape(QFrame.NoFrame)
        self.statusFrm.setFrameShadow(QFrame.Raised)
        self.statusFrm.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.statusFrm)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.statusLbl = QLabel(self.statusFrm)
        self.statusLbl.setObjectName(u"statusLbl")
        self.statusLbl.setFont(font1)

        self.horizontalLayout_2.addWidget(self.statusLbl)

        self.copyLbl = QLabel(self.statusFrm)
        self.copyLbl.setObjectName(u"copyLbl")
        self.copyLbl.setMinimumSize(QSize(150, 0))
        self.copyLbl.setMaximumSize(QSize(150, 16777215))
        self.copyLbl.setFont(font1)
        self.copyLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.copyLbl)


        self.verticalLayout.addWidget(self.statusFrm)

        main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 451, 21))
        main.setMenuBar(self.menubar)

        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"MainWindow", None))
        self.logoLbl.setText("")
        self.titleLbl.setText(QCoreApplication.translate("main", u"Title", None))
        self.verLbl.setText(QCoreApplication.translate("main", u"1.0.0", None))
        self.dropLbl.setText(QCoreApplication.translate("main", u"Drop SRT f\u200cile here", None))
        self.fixCbox.setText(QCoreApplication.translate("main", u"Replace \u00ab\u064a\u00bb with \u00ab\u06cc\u00bb and \u00ab\u0643\u00bb with \u00ab\u06a9\u00bb", None))
        self.statusLbl.setText(QCoreApplication.translate("main", u"Ready.", None))
        self.copyLbl.setText(QCoreApplication.translate("main", u"\u00a9 LeoMoon Studios", None))
    # retranslateUi
