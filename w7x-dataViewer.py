# /*
#  * ******************** BEGIN LICENSE BLOCK *********************************
#  *
#  * w7x-dataViewer
#  * Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
#  * All rights reserved
#  *
#  * github: https://github.com/alekseybeletskii
#  *
#  * The w7x-dataViewer software serves for visualization and simple processing
#  * of any data recorded with Analog Digital Converters in binary or text form.
#  *
#  * Commercial support is available. To find out more contact the author directly.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions are met:
#  *
#  *     1. Redistributions of source code must retain the above copyright notice, this
#  *          list of conditions and the following disclaimer.
#  *     2. Redistributions in binary form must reproduce the above copyright notice,
#  *         this list of conditions and the following disclaimer in the documentation
#  *         and/or other materials provided with the distribution.
#  *
#  * The software is distributed to You under terms of the GNU General Public
#  * License. This means it is "free software". However, any program, using
#  * ADCDataViewer _MUST_ be the "free software" as well.
#  * See the GNU General Public License for more details
#  * (file ./COPYING in the root of the distribution
#  * or website <http://www.gnu.org/licenses/>)
#  *
#  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  *
#  * ******************** END LICENSE BLOCK ***********************************
#  */
#


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# convert firstgui.ui to Python code:
# pyuic5 -x name.ui -o name.py

import os.path as ospath

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import  QtGui, QtWidgets

# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import mainLayout  # This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Design
import sys
# from PyQt5 import QtGui

import numpy as np

import pandas as pd

import MDSplus as m

import pyqtgraph as pg


from w7xDataSpectrogram import w7xSpectrogram

from scipy.signal import savgol_filter

class mainApp(QtWidgets.QMainWindow, mainLayout.Ui_MainWindow):

    def __init__(self):

        super(self.__class__, self).__init__()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
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

        self.actionClear.triggered.connect(self.clearAll)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft=0
        self.xRight=0

        self.redraw.clicked.connect(self.drawPlotsFromMdsplus)
        self.redrawSpectrogramUI.clicked.connect(self.drawSpectrogram)


    def drawSpectrogram(self):
        w7xSpectr = w7xSpectrogram(self)
        w7xSpectr.show()
        w7xSpectr.setDataToSpectrogram(self.d[0][self.xLeft:self.xRight])
        w7xSpectr.drawSpectrogram()

        # for i in self.d:
        #       w7xSpectr.drawSpectrogram(self.d[i][self.xLeft:self.xRight])



    def readChannelsList(self):

        # text_file = open("channelslist.txt", "r")
        # self.channelsList = text_file.readlines()

        with open('channelslist.txt', 'r') as text_file:
            self.channelsList = text_file.read().splitlines()
            # for i in range(len(self.channelsList)):
            #     self.channelsList[i]=self.channelsList[i].replace(":","-")


    def clearAll(self):
        self.plot.clear()
        self.files.clear()
        self.d.clear()
        self.t.clear()
        self.nextPen = 0
        self.channelsList.clear()
        self.xLeft=0
        self.xRight=0

    def openCsv(self):
        self.clearAll()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        #        files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
        self.files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, None, "QFileDialog.getOpenFileNames()", "All Files (*)",
                                                     "All Files (*)", options=options)

    def drawPlotsFromCsv(self):
        for i in range(len(self.files)):
            self.nextPen = self.nextPen + 1
            self.df = pd.read_csv(self.files[i], names=['x', 'y'], header=None)
            self.plot.plot(self.df['x'], self.df['y'], pen=self.nextPen)
            # print(self.files[i])
            # print(type(self.df))



    def openMdsplusQXT(self):
        self.clearAll()
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

        self.clearAll()
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
        self.nextPen=0
        for i in range(len(self.d)):

            signal = self.d[i]
            # time = list(range(len(signal)))
            time = self.t[i]
            self.nextPen = self.nextPen + 1
            self.plot.plot(time,signal, pen=(self.nextPen))
            self.getXaxisLimits()
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.xLeft = self.xLeft if self.xLeft > 0 else 0
            self.xRight = self.xRight if self.xRight < len(signal) else len(signal) - 1
            signal = signal[self.xLeft:self.xRight]
            time = time[self.xLeft:self.xRight]
            if self.SGFilt.checkState() and not self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
                self.plot.clear()
                # self.plot.plot(time, signal, pen=(self.nextPen),)
                # signal=signal[xLeft:xRight]
                # time=time[xLeft:xRight]
                self.plot.plot(time, signal, pen=(self.nextPen),)
                smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
                self.plot.plot(time, smoothed, pen=0)
            if self.SGFilt.checkState() and  self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
                self.plot.clear()
                smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
                self.d[i][self.xLeft:self.xRight] = signal = signal-smoothed
                self.plot.plot(time, signal, pen=(self.nextPen),)
                smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
                self.plot.plot(time, smoothed, pen=0)
            if self.SGFilt.checkState() and self.replaceWithSGFilt.checkState():
                self.replaceWithSGFilt.setChecked(False)
                self.plot.clear()
                smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
                self.d[i][self.xLeft:self.xRight] = signal = smoothed
                self.plot.plot(time, signal, pen=(self.nextPen),)
                smoothed = self.savitzky_golay_filt(signal,int(self.winLength.text()),int(self.polyOrder.text()))
                self.plot.plot(time, smoothed, pen=0)




    def getXaxisLimits(self):
        axX = self.plot.plotItem.getAxis('bottom')
        self.xLeft = int(axX.range[0])
        self.xRight = int(axX.range[1])
        # axY = self.plot.plotItem.getAxis('left')
        print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
        # print('y axis range: {}'.format(axY.range))  # <------- get range of y axis

    def savitzky_golay_filt(self,data, window_length=1001, polyorder=0, deriv=0, delta=1.0, axis=-1, mode='interp'):
        return savgol_filter(data,window_length,polyorder,mode=mode)


    def exitApp(self):
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
