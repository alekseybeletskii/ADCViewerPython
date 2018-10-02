import os.path as ospath
import numpy as np

class ExportToTxt:
    def __init__(self, callingObj):

        self.callingObj = callingObj

    def export_to_csv_v1(self):

        here = ospath.dirname(ospath.realpath(__file__))
        subdir = "exported"

        for i in range(len(self.callingObj.dataIn)):
            # filename = str(i) + ".csv"
            filename = self.callingObj.channelsList[i] + ".csv"
            filepath = ospath.join(here, subdir, filename.replace(":","-"))
            signal = self.callingObj.dataIn[i]
            # time = self.callingObj.dti[i]
            time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
            xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1
            np.savetxt(filepath, np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T, delimiter=', ')

        print('data exported to csv files')

    def export_to_csv_v2(self):

        here = ospath.dirname(ospath.realpath(__file__))
        subdir = "exported"

        for i in range(len(self.callingObj.dataIn)):
            filename = self.callingObj.channelsList[i]
            filepath = ospath.join(here, subdir, filename.replace(":","-"))
            signal = self.callingObj.dataIn[i]
            # time = self.callingObj.dti[i]
            time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])

            xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1

            np.savetxt(filepath + "_time_" + ".csv", time[xLeft:xRight])
            np.savetxt(filepath + "_data_" + ".csv", signal[xLeft:xRight])

            # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
            # df.to_csv(filename, header=None, index=None)

        print('data exported to csv files, time separated')
