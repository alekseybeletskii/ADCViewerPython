import numpy as np
import MDSplus as mdspl
# from datetime import datetime
class ImportFromMdsplus:

    # QOC:
    # mdpid = 171207017  # PCI saw activity here
    # mdpid = 180823005
    # conn = MDSplus.Connection(MDSconnect)
    # conn.openTree('w7x', mdpid)
    # MDSraw = conn.get('\W7X::TOP.QOC.DATAET2CH16')
    # dat_raw = MDSraw.data()
    # fs = np.int(conn.get('\W7X::TOP.QOC.HARDWARE:ACQ2106_064:CLOCK'))
    # t_raw = np.double(MDSraw.dim_of().data()) / fs
    # fs = np.int(self.mdsConnection.get('HARDWARE:ACQ2106_064:CLOCK'))
    # MDSraw = self.mdsConnection.get('DATA:DET2CH16')
    # dat_raw = MDSraw.data()
    # t_raw = np.double(dat_raw.dim_of())/fs
    # print('data loaded from mdsplus QOC')

    #==============

    # QXT:
    # self.mdsConnection.openTree('qxt1', 180816020)
    # self.mdsConnection.openTree('qxt1', 171123027)
    # self.mdsConnection.openTree('qxt1', 171123034)
    # dat_raw = self.mdsConnection.get('DATA:CH84')
    # signal = self.mdsConnection.get(f'DATA:{self.callingObj.dataInLabels[i]}')
    # dat_raw = np.double(signal.data())
    # t_raw = signal.dim_of()
    # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000).second
    # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000)
    # #print(startDataTime.strftime('%Y-%m-%d %H:%M:%S'))
    # print('data loaded from mdsplus QXT')

    def __init__(self, callingObj):
        self.callingObj = callingObj
        self.mdsConnection = mdspl.Connection('mds-data-1')
        # self.mdsConnection = mdspl.Connection('ssh://user@mds-trm-1.ipp-hgw.mpg.de')

    def getMdsplusData(self, dataLabel, treeName, shotNum, startSecond, endSecond, resample):

        self.mdsConnection.get(self.setTimeContext(startSecond, endSecond, resample))
        self.mdsConnection.openTree(treeName, shotNum)

        dat_raw = np.asarray(self.mdsConnection.get(f'DATA:{dataLabel}'))
        t_raw = self.mdsConnection.get(f'DIM_OF(DATA:{dataLabel})')
        dt = abs(np.double(t_raw[len(t_raw)-1]-t_raw[len(t_raw)-2]))*1e-9
        return dat_raw, dt

    def setTimeContext(self, start, end, resample):
        settimecontext = f'SETTIMECONTEXT({start},{end},{resample}Q)'
        if resample == '*':
            settimecontext = f'SETTIMECONTEXT({start},{end},*)'
        return settimecontext

    # def readDataLabels(self,fileName):
    #     with open(fileName, 'r') as text_file:
    #         self.callingObj.dataInLabels = text_file.read().splitlines()

    def readDatainLabels(self):
        dataInLabels = []
        fileName = 'importExport/DatainLabelsFile.txt'
        with open(fileName, 'r') as txtFile:
            for line in txtFile:
                if not line[0] == '#':
                    dataInLabels.append(line.strip())
                    # print(' self.callingObj.dataInLabels: ')
            # print( self.callingObj.dataInLabels)
        return dataInLabels
