#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:58:34 2017

@author: a
"""

#from PyQt5 import QtGui,QtCore
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import mainLayout # This file holds our MainWindow and all design related things 
              # it also keeps events etc that we defined in Qt Design
import sys 
from PyQt5 import QtGui

import numpy as np

import pandas as pd
    

class mainApp(QtGui.QMainWindow, mainLayout.Ui_MainWindow):

     def __init__(self):
#        self.df=pd
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        self.actionOpen.triggered.connect(self.openFiles)
        self.actionClear.triggered.connect(self.clearPlots)
        
#        plotexample(self)


     def clearPlots(self):
         self.plot.clear()
    

    
     def openFiles(self):
    
    #        files, _ = QFileDialog.getOpenFileNames()
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
    #        files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
    #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
            files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "All Files (*)","All Files (*)", options=options)
            if files:
                for i in range(len(files)):
    #            print(files)
                 df=pd.read_csv(files[i],names=['x', 'y'],header=None)
    #            self.plot.plot(df['x'],df['y'])
                 self.plot.plot(df['x'],df['y'],pen=(i,len(files)))
        #            print(df['x'])
       
            

def main():
    app = QtGui.QApplication(sys.argv)
    window = mainApp()
    window.show()
    sys.exit(app.exec_())




if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function