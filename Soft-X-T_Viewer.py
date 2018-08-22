#!/usr/bin/env python3
# -*- coding: utf-8 -*-



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
        self.nextPen = 0


        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.actionOpen_csv.triggered.connect(self.openCsv)
        self.actionDrawPlotsFromCsv.triggered.connect(self.drawPlotsFromCsv)
        self.actionOpen_mdsplus.triggered.connect(self.openMdsplus)
        self.actionDrawPlotsFromMdsplus.triggered.connect(self.drawPlotsFromMdsplus)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v2)



        self.actionClear.triggered.connect(self.clearPlots)
        self.actionExit.triggered.connect(self.exitApp)

    #        plotexample(self)

    def clearPlots(self):
        self.plot.clear()
        self.files.clear()
        self.d.clear()
        self.t.clear()
        self.nextPen = 0

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

    def openMdsplus(self):

        tQ = self.timeScale.text()
        tQ = tQ+'Q' if len(tQ) > 0 else '1000000000'+'Q'
        tQ = "SETTIMECONTEXT(*,*,"+tQ+")"

        # c = m.Connection('mds-data-1')
        c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get(tQ)
        # c.get('SETTIMECONTEXT(*,*,10000Q)')
        # c.openTree('qxt1', 180816020)
        # c.openTree('qxt1', 171123034)
        c.openTree('qxt1', 171123027)



# менять каналы и время здесь
# ==============================================
# data
        self.d.append(c.get('DATA:CH83'))
        # self.d.append(c.get('DATA:CH83'))
# time
        self.t.append(c.get('DIM_OF(DATA:CH83)'))
#         self.t.append(c.get('DIM_OF(DATA:CH83)'))


# ==============================================
        print('data loaded from mdsplus')
    def export_to_csv_v1(self):
        # output to file

        axX = self.plot.plotItem.getAxis('bottom')
        xLeft = int(axX.range.pop(0))
        xRight = int(axX.range.pop(0))
        # print(xLeft)
        # print(xRight)

        for i in range(len(self.d)):
            filename = str(i)  + ".csv"
            signal = self.d[i]
            time = self.t[i]

            xLeft = xLeft if xLeft > 0 else 0
            xRight = xRight if xRight < len(signal) else len(signal)-1
            np.savetxt(filename, np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T, delimiter=', ')
        print(xLeft)
        print(xRight)
        print('data exported to csv files')

    def export_to_csv_v2(self):
        # output to file

        axX = self.plot.plotItem.getAxis('bottom')
        xLeft = int(axX.range.pop(0))
        xRight = int(axX.range.pop(0))
        # print(xLeft)
        # print(xRight)

        for i in range(len(self.d)):
            filename = str(i)
            signal = self.d[i]
            time = self.t[i]

            xLeft = xLeft if xLeft > 0 else 0
            xRight = xRight if xRight < len(signal) else len(signal)-1

            np.savetxt(filename+"_data_"+".csv", time[xLeft:xRight])
            np.savetxt(filename+"_time_"+".csv", signal[xLeft:xRight])

            # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
            # df.to_csv(filename, header=None, index=None)




        print(xLeft)
        print(xRight)
        print('data exported to csv files')


    def drawPlotsFromMdsplus(self):
        for i in range(len(self.d)):
            signal = self.d[i]
            time = list(range(len(signal)))
            # time = self.t[i]
            self.nextPen = self.nextPen + 1
            # self.plot.plot(time,signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.plot.plot(time,signal, pen=(self.nextPen))

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
