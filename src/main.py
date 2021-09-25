#-*- coding: utf-8 -*-

#todo

import sys
import time #date and time
import os.path #file check
# import platform #detect os platform
from ext.darkdetect import isDark #darkdetect 0.5.0 [ https://github.com/albertosottile/darkdetect ] 20210912
# from pathlib import Path #home directory
from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff
#local imports
from gui.guiMain import Ui_main

#version: 2.0.5

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

title = 'LeoMoon SubFix'
ver = '1.0.0'

class mainUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.themeFlg = False
        self.setAcceptDrops(True) #accept file drops
        self.ui = Ui_main()
        self.ui.setupUi(self)
		#disable resizing
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle(title)
        self.ui.titleLbl.setText(title)
        self.ui.verLbl.setText('v'+ver)
        self.ui.dropLbl.setStyleSheet("QLabel {color:grey;}")
        self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 15, QtGui.QFont.Black))
        self.ui.dropLbl.setFont(QtGui.QFont('Vazir', 30, QtGui.QFont.Black))
        #prepare status bar
        self.ui.statusLbl.setText('Ready.')
        # self.ui.copyLbl.setOpenExternalLinks(True)
        # self.ui.copyLbl.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.ui.copyLbl.setText('© LeoMoon Studios')
        # self.ui.copyLbl.setText('<a style="text-decoration:none; color: inherit;" href="http://leomoon.com">© LeoMoon Studios</a>')
        if isDark():
            self.themeFlg = False
            self._theme()
        if sys.platform.startswith('darwin'): #macos
            self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 20, QtGui.QFont.Black))
            self.ui.dropLbl.setFont(QtGui.QFont('Vazir', 40, QtGui.QFont.Black))
            self.ui.verLbl.setFont(QtGui.QFont('Vazir', 13))
            self.ui.fixCbox.setFont(QtGui.QFont('Vazir', 13))
            self.ui.copyLbl.setFont(QtGui.QFont('Vazir', 13))
            self.ui.statusLbl.setFont(QtGui.QFont('Vazir', 13))

    ###############################################################################
    ####### File Drop #############################################################
    ###############################################################################
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            try:
                event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
                for url in event.mimeData().urls():
                    if os.path.isfile(str(url.toLocalFile())):
                        self._convert(str(url.toLocalFile())) #call _convert for every file
            except Exception as error:
                event.ignore()
        else:
            event.ignore()

    ###############################################################################
    ####### Functions #############################################################
    ###############################################################################
    def _theme(self):
        if not self.themeFlg:
            dark_theme = QtGui.QPalette()
            dark_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(55,53,53))
            dark_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(30,30,30))
            dark_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(55,55,55))
            dark_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Link, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(18,131,220))
            dark_theme.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            dark_theme.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53))
            QtGui.QGuiApplication.setPalette(dark_theme)
            self.setStyleSheet("""
                                    QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #5e5b5b, stop:1 #373535); border-radius: 0px;}
                                    QLabel#titleLbl {color: rgb(227,227,227);}
                                    QLabel#verLbl {color: rgb(227,227,227);}
                                        """)
            # self.ui.actionDarkMode.setChecked(True)
        else:
            light_theme = QtGui.QPalette()
            light_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Link, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(18,131,220))
            light_theme.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
            light_theme.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(243,243,243))
            QtGui.QGuiApplication.setPalette(light_theme)
            self.setStyleSheet("""
                                    QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}
                                    QLabel#titleLbl {color: rgb(68,68,68);}
                                    QLabel#verLbl {color: rgb(68,68,68);}
                                        """)
            # self.ui.actionDarkMode.setChecked(False)
        self.themeFlg = not self.themeFlg

    def _convert(self, cfile, fencoding='windows-1256', tencoding='UTF-8'):
        cdir = os.path.dirname(cfile)
        cname = os.path.splitext(os.path.basename(cfile))[0]
        cext = os.path.splitext(os.path.basename(cfile))[1]
        nfile = cdir+'/'+cname+'_fixed'+cext
        with open(cfile, 'r', encoding=fencoding) as fr:
            try:
                with open(nfile, 'w', encoding=tencoding) as fw:
                    for line in fr:
                        if self.ui.fixCbox.isChecked():
                            line = line.replace('ي','ی').replace('ك','ک')
                        fw.write(line[:-1]+'\n')
                self.ui.statusLbl.setText('<span style="color:#228B22;">All done ['+time.strftime('%H:%M:%S')+']'+'</span>')
            except ValueError as e:
                self.ui.statusLbl.setText('<span style="color:#CD5C5C;">Encoding not supported ['+time.strftime('%H:%M:%S')+']'+'</span>')

    def _exit(self):
        self.close()

    def closeEvent(self, event):
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir.ttf') #add custom font to install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Black.ttf') #add custom font to install
    main = mainUi()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
