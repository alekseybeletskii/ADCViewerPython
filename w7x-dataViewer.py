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

from scipy.signal import savgol_filter

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

        self.fs = self.samplingRate_kHz.text()
        self.actionOpen_csv.triggered.connect(self.openCsv)
        self.actionDrawPlotsFromCsv.triggered.connect(self.drawPlotsFromCsv)
        self.actionOpen_mdsplus_QXT.triggered.connect(self.openMdsplusQXT)
        self.actionOpen_mdsplus_QOC.triggered.connect(self.openMdsplusQOC)
        self.actionDrawPlotsFromMdsplus.triggered.connect(self.drawPlotsFromMdsplus)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v1)
        self.actionExport_time_to_separate_file.triggered.connect(self.export_to_csv_v2)

        self.actionClear.triggered.connect(self.clearPlots)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft=0
        self.xRight=0

        self.redraw.clicked.connect(self.drawPlotsFromMdsplus)



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
        self.files, _ = QFileDialog.getOpenFileNames(self, None, "QFileDialog.getOpenFileNames()", "All Files (*)",
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
        # self.clearPlots()
        self.readChannelsList()

        c = m.Connection('mds-data-1')
        # c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get(self.setTimeContext())
        # c.get('SETTIMECONTEXT(*,*,10000Q)')
        # c.openTree('qxt1', 180816020)
        # c.openTree('qxt1', 171123034)

        shotNumber = self.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 171123034
        self.shot.setText(str(shotNumber))
        c.openTree('qxt1', shotNumber)

        for i in range(len(self.channelsList)):
            # dat_raw = c.get('DATA:CH84')
            dat_raw = c.get(f'DATA:{self.channelsList[i]}')
            # t_raw = c.get(f'DIM_OF(DATA:{self.channelsList[i]})')
            t_raw = np.double(dat_raw.dim_of().data())

            self.d.append(dat_raw)
            self.t.append(t_raw)

        print('data loaded from mdsplus')
        # print('fs: ',self.fs)

    def setTimeContext(self):
        resample = int(self.resampling.text())
        settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
        if resample < 0:
            resample = '1000000'
            settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
            self.timeScale.setText(str(resample))
        if resample == 1:
            settimecontext = "SETTIMECONTEXT(*,*,*)"
        return settimecontext

    def openMdsplusQOC(self):
        # mdpid = 171207017  # PCI saw activity here
        # mdpid = 180823005
        #
        # conn = MDSplus.Connection(MDSconnect)
        # conn.openTree('w7x', mdpid)
        # MDSraw = conn.get('\W7X::TOP.QOC.DATAET2CH16')
        # dat_raw = MDSraw.data()
        # fs = np.int(conn.get('\W7X::TOP.QOC.HARDWARE:ACQ2106_064:CLOCK'))
        # t_raw = np.double(MDSraw.dim_of().data()) / fs

        # self.clearPlots()
        self.readChannelsList()

        shotNumber = self.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 180823005
        self.shot.setText(str(shotNumber))

        c = m.Connection('mds-data-1')
        #        c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')

        c.get(self.setTimeContext())


        c.openTree('qoc', shotNumber)
        # fs = np.int(c.get('HARDWARE:ACQ2106_064:CLOCK'))

        for i in range(len(self.channelsList)):
            # MDSraw = c.get('DATA:DET2CH16')
            dat_raw = c.get(f'DATA:{self.channelsList[i]}')
            # dat_raw = MDSraw.data()
            t_raw = np.double(dat_raw.dim_of())
            # t_raw = np.double(dat_raw.dim_of())/fs

            # dat_raw = c.get(f'DATA:{self.channelsList[i]}')
            # t_raw = c.get(f'DIM_OF(DATA:{self.channelsList[i]})')

            self.d.append(dat_raw)
            self.t.append(t_raw)

        print('data loaded from mdsplus')
        # print('fs: ',fs)

    def export_to_csv_v1(self):
        # output to file


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

            xLeft = self.xLeft if self.xLeft > 0 else 0
            xRight = self.xRight if self.xRight < len(signal) else len(signal) - 1
            np.savetxt(filepath, np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T, delimiter=', ')

        print('data exported to csv files')

    def export_to_csv_v2(self):
        # output to file


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

            xLeft = self.xLeft if self.xLeft > 0 else 0
            xRight = self.xRight if self.xRight < len(signal) else len(signal) - 1

            np.savetxt(filepath + "_time_" + ".csv", time[xLeft:xRight])
            np.savetxt(filepath + "_data_" + ".csv", signal[xLeft:xRight])

            # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
            # df.to_csv(filename, header=None, index=None)

        print('data exported to csv files, time separated')

    def drawPlotsFromMdsplus(self):
        self.plot.clear()
        for i in range(len(self.d)):
            signal = self.d[i]
            # time = list(range(len(signal)))
            time = self.t[i]
            self.nextPen = self.nextPen + 1
            # self.plot.plot(time,signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.plot.plot(time, signal, pen=(self.nextPen),)
            if self.SGFilt.checkState():
               smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
               self.plot.plot(time, smoothed, pen=0)

        axX = self.plot.plotItem.getAxis('bottom')
        self.xLeft = int(axX.range[0])
        self.xRight = int(axX.range[1])
        print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
        axY = self.plot.plotItem.getAxis('left')
        print('y axis range: {}'.format(axY.range))  # <------- get range of y axis

    def savitzky_golay_filt(self,data, window_length=1001, polyorder=0, deriv=0, delta=1.0, axis=-1, mode='interp'):
        return savgol_filter(data,window_length,polyorder,mode=mode)

def main():
    app = QtGui.QApplication(sys.argv)
    window = mainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
