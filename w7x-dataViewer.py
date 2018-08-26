#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os.path as ospath

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import mainLayout  # This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Design
import sys
from PyQt5 import QtGui

import numpy as np

import pandas as pd

import MDSplus as m


class mainApp(QtGui.QMainWindow, mainLayout.Ui_MainWindow):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.files = []
        self.d = []
        self.t = []
        self.channelsList = []
        self.nextPen = 0

        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.actionOpen_csv.triggered.connect(self.openCsv)
        self.actionDrawPlotsFromCsv.triggered.connect(self.drawPlotsFromCsv)
        self.actionOpen_mdsplus_QXT.triggered.connect(self.openMdsplusQXT)
        self.actionOpen_mdsplus_QOC.triggered.connect(self.openMdsplusQOC)
        self.actionDrawPlotsFromMdsplus.triggered.connect(self.drawPlotsFromMdsplus)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v1)
        self.actionExport_time_to_separate_file.triggered.connect(self.export_to_csv_v2)

        self.actionClear.triggered.connect(self.clearPlots)
        self.actionExit.triggered.connect(self.exitApp)

    #        plotexample(self)

    def readChannelsList(self):

        # text_file = open("channelslist.txt", "r")
        # self.channelsList = text_file.readlines()

        with open('channelslist.txt', 'r') as text_file:
            self.channelsList = text_file.read().splitlines()
            # for i in range(len(self.channelsList)):
            #     self.channelsList[i]=self.channelsList[i].replace(":","-")


    def clearPlots(self):
        self.plot.clear()
        self.files.clear()
        self.d.clear()
        self.t.clear()
        self.nextPen = 0
        self.channelsList.clear()

    def openCsv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #        files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
        self.files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "All Files (*)",
                                                     "All Files (*)", options=options)

    def drawPlotsFromCsv(self):
        for i in range(len(self.files)):
            self.nextPen = self.nextPen + 1
            self.df = pd.read_csv(self.files[i], names=['x', 'y'], header=None)
            self.plot.plot(self.df['x'], self.df['y'], pen=self.nextPen)
            # print(self.files[i])
            # print(type(self.df))

    def exitApp(self):
        sys.exit()

    def openMdsplusQXT(self):
        self.clearPlots()
        self.readChannelsList()

        tQ = self.timeScale.text()
        tQ = tQ if int(tQ) > 0 else '1000000000'
        self.timeScale.setText(tQ)
        tQ = "SETTIMECONTEXT(*,*," + tQ + "Q)"

        c = m.Connection('mds-data-1')
        # c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get(tQ)
        # c.get('SETTIMECONTEXT(*,*,10000Q)')
        # c.openTree('qxt1', 180816020)
        # c.openTree('qxt1', 171123034)

        shotNumber = self.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 171123034
        self.shot.setText(str(shotNumber))
        c.openTree('qxt1', shotNumber)

        for i in range(len(self.channelsList)):
            self.d.append(c.get(f'DATA:{self.channelsList[i]}'))
            self.t.append(c.get(f'DIM_OF(DATA:{self.channelsList[i]})'))

        print('data loaded from mdsplus')

    def openMdsplusQOC(self):
        self.clearPlots()
        # mdpid = 171207017  # PCI saw activity here
        # mdpid = 180823005

        self.readChannelsList()

        tQ = self.timeScale.text()
        tQ = tQ if int(tQ) > 0 else '1000000000'
        self.timeScale.setText(tQ)
        tQ = "SETTIMECONTEXT(*,*," + tQ + "Q)"

        shotNumber = self.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 180823005
        self.shot.setText(str(shotNumber))

        c = m.Connection('mds-data-1')
#        c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')

        c.get(tQ)

        c.openTree('qoc', shotNumber)
        fs = np.int(c.get('HARDWARE:ACQ2106_064:CLOCK'))

        for i in range(len(self.channelsList)):
            # MDSraw = c.get('DATA:DET2CH16')
            # MDSraw = c.get(f'DATA:{self.channelsList[i]}')
            # dat_raw = MDSraw.data()
            # t_raw = np.double(MDSraw.dim_of().data()) / fs

            dat_raw = c.get(f'DATA:{self.channelsList[i]}')
            t_raw = c.get(f'DIM_OF(DATA:{self.channelsList[i]})')

            self.d.append(dat_raw)
            self.t.append(t_raw)

        print('data loaded from mdsplus')
        print('fs: ',fs)

    def export_to_csv_v1(self):
        # output to file

        axX = self.plot.plotItem.getAxis('bottom')
        xLeft = int(axX.range[0])
        xRight = int(axX.range[1])
        # print(xLeft)
        # print(xRight)

        # get the current script path.
        here = ospath.dirname(ospath.realpath(__file__))
        subdir = "exported"

        for i in range(len(self.d)):
            # filename = str(i) + ".csv"
            filename = self.channelsList[i] + ".csv"
            filepath = ospath.join(here, subdir, filename.replace(":","-"))
            signal = self.d[i]
            time = self.t[i]

            xLeft = xLeft if xLeft > 0 else 0
            xRight = xRight if xRight < len(signal) else len(signal) - 1
            np.savetxt(filepath, np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T, delimiter=', ')
        print('xLeft: ',xLeft)
        print('xRight: ',xRight)
        print('data exported to csv files')

    def export_to_csv_v2(self):
        # output to file

        axX = self.plot.plotItem.getAxis('bottom')
        xLeft = int(axX.range[0])
        xRight = int(axX.range[1])
        # print(xLeft)
        # print(xRight)

        # get the current script path.
        here = ospath.dirname(ospath.realpath(__file__))
        subdir = "exported"

        for i in range(len(self.d)):
            filename = self.channelsList[i]
            filepath = ospath.join(here, subdir, filename.replace(":","-"))
            signal = self.d[i]
            time = self.t[i]

            xLeft = xLeft if xLeft > 0 else 0
            xRight = xRight if xRight < len(signal) else len(signal) - 1

            np.savetxt(filepath + "_time_" + ".csv", time[xLeft:xRight])
            np.savetxt(filepath + "_data_" + ".csv", signal[xLeft:xRight])

            # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
            # df.to_csv(filename, header=None, index=None)

        print('xLeft: ',xLeft)
        print('xRight: ',xRight)
        print('data exported to csv files')

    def drawPlotsFromMdsplus(self):
        for i in range(len(self.d)):
            signal = self.d[i]
            time = list(range(len(signal)))
            # time = self.t[i]
            self.nextPen = self.nextPen + 1
            # self.plot.plot(time,signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.plot.plot(time, signal, pen=(self.nextPen))

        axX = self.plot.plotItem.getAxis('bottom')
        print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
        axY = self.plot.plotItem.getAxis('left')
        print('y axis range: {}'.format(axY.range))  # <------- get range of y axis


def main():
    app = QtGui.QApplication(sys.argv)
    window = mainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
