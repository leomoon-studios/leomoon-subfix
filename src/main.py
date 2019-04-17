#!usr/bin/env python
#-*- coding: utf-8 -*-

#todo

import sys
import time #date and time
import os.path #file check
import platform #detect os platform
from os import stat, remove #decrypt
import random
from pathlib import Path #home directory
from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff
#local imports
from gui.guiMain import Ui_main

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class mainUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.title = 'LeoMoon SubFix'
        self.ver = '2.0.0'
        QtWidgets.QWidget.__init__(self, None)
        self.setAcceptDrops(True) #accept file drops
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.setFixedSize(401, 286) #no resize
        self.setWindowTitle(self.title)
        self.ui.titleLbl.setText(self.title)
        self.ui.verLbl.setText('v'+self.ver)
        self.ui.verLbl.setStyleSheet("QLabel {color:white;}")
        self.ui.dropLbl.setStyleSheet("QLabel {color:grey;}")
        self.statusBar().setSizeGripEnabled(False) #disable resize arrow
        #prepare status bar
        self.ui.statusLbl.setText('<span style="color:black;">Ready.</span>')
        self.ui.copyLbl.setOpenExternalLinks(True)
        self.ui.copyLbl.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.ui.copyLbl.setText('<a style="text-decoration:none; color: inherit;" href="http://leomoon.com">© LeoMoon Studios</a>')
        #font = QtGui.QFont()
        #font.setFamily('Tahoma')
        #font.setPointSize(10)
        #os dependent ui
        if sys.platform.startswith('darwin'): #macos
            self.ui.titleLbl.setFont(QtGui.QFont('Tahoma', 18, QtGui.QFont.Bold))
            self.ui.dropLbl.setFont(QtGui.QFont('Tahoma', 30, QtGui.QFont.Bold))
            self.ui.verLbl.setFont(QtGui.QFont('Tahoma', 13))
            self.ui.fixCbox.setFont(QtGui.QFont('Tahoma', 13))
            self.ui.copyLbl.setFont(QtGui.QFont('Tahoma', 13))
            self.ui.statusLbl.setFont(QtGui.QFont('Tahoma', 13))
        
    ###############################################################################
    ####### Variables #############################################################
    ###############################################################################
    

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
    ####### File Manipulation #####################################################
    ###############################################################################

    def _dropOpen(self):
        self.ui.decFileInp.setText('') #set text to nothing first
        self.filename = self.dropname
        if self.filename and os.path.exists(self.filename[0]):
            self.ui.encFileInp.setText(self.filename[0])
            self.ui.decFileInp.setText(self.filename[0])
        else:
            self.ui.editorEdit.setFocus()

    ###############################################################################
    ####### Functions #############################################################
    ###############################################################################

    def _convert(self, cfile, fencoding='windows-1256', tencoding='UTF-8'):
        #print(cfile)
        cdir = os.path.dirname(cfile)
        cname = os.path.splitext(os.path.basename(cfile))[0]
        cext = os.path.splitext(os.path.basename(cfile))[1]
        #print(os.path.basename(cfile)) #filename with extension
        #print(cdir) #folder name
        #print(cname) #filename only
        #print(cext) #extension only
        nfile = cdir+'/'+cname+'_fixed'+cext
        with open(cfile, 'r', encoding=fencoding) as fr:
            try:
                with open(nfile, 'w', encoding=tencoding) as fw:
                    for line in fr:
                        if self.ui.fixCbox.isChecked():
                            line = line.replace('ي','ی').replace('ك','ک')
                        fw.write(line[:-1]+'\n')
                print('done')
                self.ui.statusLbl.setText('<span style="color:green;">All done ['+time.strftime('%H:%M:%S')+']'+'</span>')
            except ValueError as e:
                self.ui.statusLbl.setText('<span style="color:red;">Encoding not supported ['+time.strftime('%H:%M:%S')+']'+'</span>')

    def _exit(self):
        self.close()

    def closeEvent(self, event):
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Tahoma-Bold.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Tahoma-Regular.ttf') #add custom font no install
    main = mainUi()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
