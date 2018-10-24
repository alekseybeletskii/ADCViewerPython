from os import path, makedirs
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from datetime import datetime

from PyQt5.QtGui import QScreen


class ExportToTxtImg:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.here = path.dirname(path.realpath(__file__))
        self.exportDirName = "exported"
        self.exportDirPath = path.join(self.here, '..', self.exportDirName)
        if not path.exists(self.exportDirPath):
            makedirs(self.exportDirPath)

    def export_to_csv_v1(self):



        for i in range(len(self.callingObj.dataIn)):
            # filename = str(i) + ".csv"
            filename = self.callingObj.dataInLabels[i] + ".csv"
            filepath = path.join(self.exportDirPath, filename.replace(":", "-"))

            signal = self.callingObj.dataIn[i]
            # time = self.callingObj.dti[i]
            # time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
            dti = self.callingObj.dti[i]
            time = np.arange(0, (signal.size) * dti, dti) if self.callingObj.dti[i].size==1 else dti

            xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1
            np.savetxt(filepath, np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T, delimiter=', ')

        #print('data exported to csv files')

    def export_to_csv_v2(self):



        for i in range(len(self.callingObj.dataIn)):
            filename = self.callingObj.dataInLabels[i]
            filepath = path.join(self.exportDirPath, filename.replace(":", "-"))

            signal = self.callingObj.dataIn[i]
            # time = self.callingObj.dti[i]
            # time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
            dti = self.callingObj.dti[i]
            time = np.arange(0, (signal.size) * dti, dti) if self.callingObj.dti[i].size==1 else dti
            xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0

            xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1

            np.savetxt(filepath + "_time_" + ".csv", time[xLeft:xRight])
            np.savetxt(filepath + "_data_" + ".csv", signal[xLeft:xRight])

            # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
            # df.to_csv(filename, header=None, index=None)

        #print('data exported to csv files, time separated')


    def savePlotTofile(self, x, y):

        filename = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S') + ".peaks"
        filepath = path.join(self.exportDirPath, filename.replace(":","-"))
        # peaksX = self.callingObj.allPeaksXPoints
        # peaksY = self.callingObj.allPeaksYPoints

        xy = np.array([x, y]).T
        # xy.sort(axis=0)
        # xy[np.argsort(xy[:, 0])]


        xy = xy[xy[:, 0].argsort()]

        # np.savetxt(filepath, np.array([x, y]).T, delimiter=', ')
        np.savetxt(filepath, xy, delimiter=', ')

        # pg.plot(np.arange(len(y)),y)
        # pg.plot(xy[:,0],xy[:,1],pen='r',  symbol='o' )



        #print('data exported to utcnow.peaks file')

    def exportWidgetToImg(self,widget):

        # exporter = pg.exporters.ImageExporter(widget.scene())
        # exporter.export(filepath)
        # exporter.parameters()['width'] = widget.scene().sceneRect().width()
#!!!!!!!!!!!
        # for some reason, pyqtgraph.exporters.ImageExporter deteriorates spectrogram resolution during export
        # both in exported file and in the exported widget
#!!!!!!!!!!!

        filename = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f') + ".jpg"
        filepath = path.join(self.exportDirPath, filename.replace(":","-"))
        p = widget.grab()
        p.save(filepath, 'jpg')

