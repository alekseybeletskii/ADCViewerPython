import numpy as np
import MDSplus as mdspl
# from datetime import datetime
class ImportFromMdsplus:
    def __init__(self, callingObj):
        self.callingObj = callingObj
    
    def openQXT(self):
        self.callingObj.clearAll()
        self.readChannelsList('QXTchList.txt')
        c = mdspl.Connection('mds-data-1')
        # c = mdspl.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get(self.setTimeContext())
        shotNumber = self.callingObj.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 171123034
        self.callingObj.shot.setText(str(shotNumber))
        c.openTree('qxt1', shotNumber)
        # c.openTree('qxt1', 180816020)
        # c.openTree('qxt1', 171123027)
        # c.openTree('qxt1', 171123034)

        for i in range(len(self.callingObj.channelsList)):
            dat_raw = c.get(f'DATA:{self.callingObj.channelsList[i]}')
            t_raw = c.get(f'DIM_OF(DATA:{self.callingObj.channelsList[i]})')
            # dat_raw = c.get('DATA:CH84')
            # signal = c.get(f'DATA:{self.callingObj.channelsList[i]}')
            # dat_raw = np.double(signal.data())
            # t_raw = signal.dim_of()
            # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000).second
            # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000)
            # print(startDataTime.strftime('%Y-%m-%d %H:%M:%S'))
            dti = abs(np.double(t_raw[2]-t_raw[1]))*1e-9
            self.callingObj.d.append(dat_raw)
            self.callingObj.t.append(dti)

        print('data loaded from mdsplus QXT')

    def openQOC(self):
        # mdpid = 171207017  # PCI saw activity here
        # mdpid = 180823005
        # conn = MDSplus.Connection(MDSconnect)
        # conn.openTree('w7x', mdpid)
        # MDSraw = conn.get('\W7X::TOP.QOC.DATAET2CH16')
        # dat_raw = MDSraw.data()
        # fs = np.int(conn.get('\W7X::TOP.QOC.HARDWARE:ACQ2106_064:CLOCK'))
        # t_raw = np.double(MDSraw.dim_of().data()) / fs

        self.callingObj.clearAll()
        self.readChannelsList('QOCchList.txt')
        shotNumber = self.callingObj.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 180823005
        self.callingObj.shot.setText(str(shotNumber))

        c = mdspl.Connection('mds-data-1')
        # c = mdspl.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get(self.setTimeContext())
        c.openTree('qoc', shotNumber)

        # fs = np.int(c.get('HARDWARE:ACQ2106_064:CLOCK'))

        for i in range(len(self.callingObj.channelsList)):
            dat_raw = c.get(f'DATA:{self.callingObj.channelsList[i]}')
            t_raw = c.get(f'DIM_OF(DATA:{self.callingObj.channelsList[i]})')
            print(len(t_raw))
            dti = abs(np.double(t_raw[len(t_raw)-1]-t_raw[len(t_raw)-2]))*1e-9
            self.callingObj.t.append(dti)
            self.callingObj.d.append(dat_raw)
            # MDSraw = c.get('DATA:DET2CH16')
            # dat_raw = MDSraw.data()
            # t_raw = np.double(dat_raw.dim_of())/fs

        print('data loaded from mdsplus QOC')

    def setTimeContext(self):
        resample = int(self.callingObj.resampling.text()) if self.callingObj.resampling.text().isnumeric() else 1
        settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
        if resample < 0:
            resample = '1000000'
            settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
            self.callingObj.timeScale.setText(str(resample))
        if resample == 1:
            settimecontext = "SETTIMECONTEXT(*,*,*)"
        return settimecontext

    def readChannelsList(self,fileName):
        with open(fileName, 'r') as text_file:
            self.callingObj.channelsList = text_file.read().splitlines()