import numpy as np
import MDSplus as mdspl
# from datetime import datetime
class ImportFromMdsplus:
    def __init__(self, callingObj):
        self.callingObj = callingObj
        self.mdsConnection = mdspl.Connection('mds-data-1')
        # self.mdsConnection = mdspl.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
    
    def openQXT(self):
        self.readDataLabels('importExport/QXTchList.txt')

        self.callingObj.clearAllViewer()
        self.mdsConnection.get(self.setTimeContext())
        shotNumber = self.callingObj.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 171123034
        self.callingObj.shot.setText(str(shotNumber))
        self.mdsConnection.openTree('qxt1', shotNumber)
        # self.mdsConnection.openTree('qxt1', 180816020)
        # self.mdsConnection.openTree('qxt1', 171123027)
        # self.mdsConnection.openTree('qxt1', 171123034)

        for i in range(len(self.callingObj.dataInLabels)):
            dat_raw = np.asarray(self.mdsConnection.get(f'DATA:{self.callingObj.dataInLabels[i]}'))
            t_raw = self.mdsConnection.get(f'DIM_OF(DATA:{self.callingObj.dataInLabels[i]})')
            # dat_raw = self.mdsConnection.get('DATA:CH84')
            # signal = self.mdsConnection.get(f'DATA:{self.callingObj.dataInLabels[i]}')
            # dat_raw = np.double(signal.data())
            # t_raw = signal.dim_of()
            # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000).second
            # startDataTime = datetime.utcfromtimestamp(t_raw[0] // 1000000000)
            # #print(startDataTime.strftime('%Y-%m-%d %H:%M:%S'))
            dti = abs(np.double(t_raw[len(t_raw)-1]-t_raw[len(t_raw)-2]))*1e-9
            self.callingObj.dataIn.append(dat_raw)
            self.callingObj.dti.append(dti)
            self.callingObj.frq.append(int(round(np.power(dti,-1))))

        #print('data loaded from mdsplus QXT')

    def openQOC(self):
        # mdpid = 171207017  # PCI saw activity here
        # mdpid = 180823005
        # conn = MDSplus.Connection(MDSconnect)
        # conn.openTree('w7x', mdpid)
        # MDSraw = conn.get('\W7X::TOP.QOC.DATAET2CH16')
        # dat_raw = MDSraw.data()
        # fs = np.int(conn.get('\W7X::TOP.QOC.HARDWARE:ACQ2106_064:CLOCK'))
        # t_raw = np.double(MDSraw.dim_of().data()) / fs

        self.callingObj.clearAllViewer()
        self.readDataLabels('importExport/QOCchList.txt')
        shotNumber = self.callingObj.shot.text()
        shotNumber = int(shotNumber) if len(shotNumber)==9 else 180823005
        self.callingObj.shot.setText(str(shotNumber))

        c = mdspl.Connection('mds-data-1')
        # c = mdspl.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        self.mdsConnection.get(self.setTimeContext())
        self.mdsConnection.openTree('qoc', shotNumber)

        # fs = np.int(self.mdsConnection.get('HARDWARE:ACQ2106_064:CLOCK'))


        for i in range(len(self.callingObj.dataInLabels)):
            dat_raw = np.asarray(self.mdsConnection.get(f'DATA:{self.callingObj.dataInLabels[i]}'))
            t_raw = self.mdsConnection.get(f'DIM_OF(DATA:{self.callingObj.dataInLabels[i]})')
            dti = abs(np.double(t_raw[len(t_raw)-1]-t_raw[len(t_raw)-2]))*1e-9
            self.callingObj.dataIn.append(dat_raw)
            self.callingObj.dti.append(dti)
            self.callingObj.frq.append(int(round(np.power(dti,-1))))
            # MDSraw = self.mdsConnection.get('DATA:DET2CH16')
            # dat_raw = MDSraw.data()
            # t_raw = np.double(dat_raw.dim_of())/fs

        #print('data loaded from mdsplus QOC')

    def setTimeContext(self):
        resample = int(self.callingObj.MDSresampling.text()) if self.callingObj.MDSresampling.text().isnumeric() else 1
        settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
        if resample < 0:
            resample = '1000000'
            settimecontext = "SETTIMECONTEXT(*,*," + str(resample) + "Q)"
            self.callingObj.MDSresampling.setText(str(resample))
        if resample == 1:
            settimecontext = "SETTIMECONTEXT(*,*,*)"
        return settimecontext

    def readDataLabels(self,fileName):
        with open(fileName, 'r') as text_file:
            self.callingObj.dataInLabels = text_file.read().splitlines()