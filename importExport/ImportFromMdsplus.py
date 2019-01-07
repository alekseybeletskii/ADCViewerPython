# /*
#  * ******************** BEGIN LICENSE BLOCK *********************************
#  *
#  * w7x-PyViewer
#  * Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
#  * All rights reserved
#  *
#  * github: https://github.com/alekseybeletskii
#  *
#  * The w7x-PyViewer software serves for visualization and simple processing
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
#  * w7x-PyViewer _MUST_ be the "free software" as well.
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


import numpy as np
import MDSplus as mdspl
from utils.DataResample import DataResample
from pyqtgraph import PlotDataItem as plotDataItem
from importExport.DataModel import DataModel

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
        self.allData = []


        # self.mdsConnection = mdspl.Connection('ssh://user@mds-trm-1.ipp-hgw.mpg.de')

    def openMdsPlus(self):
        start = self.callingObj.settings["startMdsplusTime"]
        end = self.callingObj.settings["endMdsplusTime"]
        resample = self.callingObj.settings["deltaMdsplusTime"]
        shotNumber = self.callingObj.settings["shotNum"]
        treeName = self.callingObj.settings["treeName"]

        dataInLabels = self.readDataLabels()

        resampler = DataResample(self)
        target_frq_Hz = self.callingObj.settings["targetFrq_kHz"] * 1000

        for i in range(len(dataInLabels)):
            data, dt = self.getMdsplusData(dataInLabels[i], treeName, shotNumber, start, end, resample)

            if self.callingObj.settings["applyDownsampling"] and self.callingObj.settings["targetFrq_kHz"] < self.callingObj.settings["fs_kHz"]:
                data = resampler.downSampleDecimate(data, 1.0 / dt, target_frq_Hz)
                dt = np.double(1.0 / target_frq_Hz)
                print('input data frequency, *AFTER* downsampling, Hz: ' + str(target_frq_Hz))

            adcChannelTimeShift = 0
            adcChannel = 0
            time = np.arange(0, (data.size) * dt, dt) + adcChannelTimeShift
            label = dataInLabels[i] + '_ch#' + str(adcChannel)
            pdi = plotDataItem(time, data, name=label)
            dataModel = DataModel(pdi, label, dt,  adcChannel, adcChannelTimeShift)
            dataModifiers = {'timeshift': 0.0, 'datamultiplier': 1.0, 'datashift': 0.0, 'independentvar': i,
                                  'datatype': 'whatever'}
            dataModel.setDataModifiers(dataModifiers)

            self.allData.append(dataModel)

        return self.allData


    def getMdsplusData(self, dataLabel, treeName, shotNum, startSecond, endSecond, resample):

        # treeName = 'QSR02'
        # shotNum = 180724058
        # dataLabel = 'TUBE08'

        switcher = {
            'qxt1': 1e-9,
            'qoc': 1e-9,
            'qsr02': 1
        }

        self.mdsConnection.get(self.setTimeContext(startSecond, endSecond, resample))
        self.mdsConnection.openTree(treeName, shotNum)

        dat_raw = np.asarray(self.mdsConnection.get(f'DATA:{dataLabel}'))
        t_raw = self.mdsConnection.get(f'DIM_OF(DATA:{dataLabel})')


        dt = abs(np.double(t_raw[len(t_raw)-1]-t_raw[len(t_raw)-2]))*switcher.get(treeName, 1)


        return dat_raw, dt

    def setTimeContext(self, start, end, resample):
        settimecontext = f'SETTIMECONTEXT({start},{end},{resample}Q)'
        if resample == '*':
            settimecontext = f'SETTIMECONTEXT({start},{end},*)'
        return settimecontext

    # def readDataLabels(self,fileName):
    #     with open(fileName, 'r') as text_file:
    #         self.callingObj.dataInLabels = text_file.read().splitlines()

    def readDataLabels(self):
        dataInLabels = []
        fileName = 'importExport/DatainLabelsFile.txt'
        with open(fileName, 'r') as txtFile:
            for line in txtFile:
                if not line[0] == '#':
                    dataInLabels.append(line.strip())
                    # print(' self.callingObj.dataInLabels: ')
            # print( self.callingObj.dataInLabels)
        return dataInLabels
