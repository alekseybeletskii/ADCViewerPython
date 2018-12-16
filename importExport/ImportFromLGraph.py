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


from PyQt5 import QtWidgets

import pandas as pd
import numpy as np
import struct
from collections import namedtuple
from os import path as ospath
from io import BytesIO


class ImportFromLGraph(QtWidgets.QMainWindow):

    def __init__(self,callingObj,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callingObj = callingObj

        self.adcSignature = ''
        self.deviceName  = ''
        self.createDateTime  = ''
        self.channelsMax  = ''
        self.realChannelsQuantity  = 0
        self.realCadresQuantity  = 0
        self.realSamplesQuantity   = 0
        self.totalTime  = 0.0
        self.adcRate  = 0.0
        self.interCadreDelay  = 0.0
        self.channelRate  = 0.0
        self.activeAdcChannelArray  = np.empty(0)
        self.adcChannelArray  = np.empty(0)
        self.adcGainArray  = np.empty(0)
        self.isSignalArray  = np.empty(0)
        self.dataFormat  = 0
        self.realCadres64  = 0
        self.adcScale  = np.empty(0)
        self.adcOffset  = np.empty(0)
        self.calibrOffset  = np.empty(0)
        self.calibrScale  = np.empty(0)
        self.segments   = 0

        self.filename = ''
        self.adcData = np.empty(0)
        self.chanAdcOrdinal = np.empty(0)
        self.chanAdcGain = np.empty(0)




    def openLGraph(self):
        self.callingObj.clearAllViewer()

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        dataFiles, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"ADC binary files", self.callingObj.latestFilePath,"*.dat;;All Files (*)", options=options)

        if dataFiles:
            self.callingObj.latestFilePath = ospath.abspath(dataFiles[0])

        for i in range(len(dataFiles)):
            path_to_dir, filename_and_ext = ospath.split(dataFiles[i])
            self.filename, _ = ospath.splitext(filename_and_ext)
            parFile = ospath.join(path_to_dir, self.filename + ".par")
            datFile = ospath.join(path_to_dir, self.filename + ".dat")

            self.readPar(parFile)

            self.getRealChannelsOrdinalAndGainadcCountsToVoltss()


            self.readDat(datFile)
            print('test...')




    def getRealChannelsOrdinalAndGainadcCountsToVoltss(self):
        switcher = {
            '0': 1,
            '1': 2,
            '2': 4,
            '3': 8
        }
        for nextCh in range(self.activeAdcChannelArray.size):
            if self.activeAdcChannelArray[nextCh] == 1:
                self.chanAdcOrdinal = np.append(self.chanAdcOrdinal, nextCh + 1)
                self.chanAdcGain = np.append(self.chanAdcGain, switcher.get(self.adcGainArray[nextCh], 1))




    def readPar(self, parFile):
        with open(parFile, "rb") as binary_parFile:
            allBytes = BytesIO(binary_parFile.read())
            self.adcSignature = allBytes.read(20).decode('utf-8').strip()
            self.deviceName = allBytes.read(17).decode('utf-8').strip()
            self.createDateTime = allBytes.read(26).decode('utf-8').strip()
            self.channelsMax = struct.unpack('<h', allBytes.read(2))[0]
            self.realChannelsQuantity = struct.unpack('<h', allBytes.read(2))[0]
            self.realCadresQuantity = struct.unpack('<i', allBytes.read(4))[0]
            self.realSamplesQuantity = struct.unpack('<i', allBytes.read(4))[0]
            self.totalTime = struct.unpack('<d', allBytes.read(8))[0]
            self.adcRate = struct.unpack('<f', allBytes.read(4))[0]
            self.interCadreDelay = struct.unpack('<f', allBytes.read(4))[0]
            self.channelRate = struct.unpack('<f', allBytes.read(4))[0]
            # In LGraph-2, "ADC rate" was somehow written equal to "channel rate",
            # but real value of "ADC rate" is  "channelRate" * "RealChannelsQuantity", or 1/("TotalTime"/"RealCadresQuantity")
            # So it is recalculated below:
            self.adcRate = self.realChannelsQuantity * self.channelRate

            for i in range(32):
                self.activeAdcChannelArray = np.append(self.activeAdcChannelArray,
                                                       int.from_bytes(allBytes.read(1), byteorder='little'))
            for i in range(32):
                self.adcChannelArray = np.append(self.adcChannelArray,
                                                 int.from_bytes(allBytes.read(1), byteorder='little'))
            for i in range(32):
                self.adcGainArray = np.append(self.adcGainArray, int.from_bytes(allBytes.read(1), byteorder='little'))
            for i in range(32):
                self.isSignalArray = np.append(self.isSignalArray, int.from_bytes(allBytes.read(1), byteorder='little'))
            self.dataFormat = struct.unpack('<i', allBytes.read(4))[0]
            self.realCadres64 = struct.unpack('<q', allBytes.read(8))[0]
            for i in range(32):
                self.adcScale = np.append(self.adcScale, struct.unpack('<d', allBytes.read(8))[0])
            for i in range(32):
                self.adcOffset = np.append(self.adcOffset, struct.unpack('<d', allBytes.read(8))[0])
            for i in range(1024):
                self.calibrOffset = np.append(self.calibrOffset, struct.unpack('<d', allBytes.read(8))[0])
            for i in range(1024):
                self.calibrScale = np.append(self.calibrScale, struct.unpack('<d', allBytes.read(8))[0])
            self.segments = struct.unpack('<i', allBytes.read(4))

    def readDat(self, datFile):
        # calibration:
        # L783: 5.12 (V)/2048(adc) = 0.0025
        # E2010: 3.31776(V)/8192(adc) = 0.000405

        indexOfADCInputRange = 0
        # index of a channel input range,
        # define what part of ADC calibration table (seems like only for e20-10 module, see e2010 programmers guide )
        # is used corresponding to input voltage range (+-3V, +-1V, +-0.3V in case of ADC e2010)


        self.adcData = np.fromfile(datFile, np.int16)

        self.adcData = np.reshape(self.adcData,(self.realCadresQuantity, self.realChannelsQuantity))

        for chan in range(self.realChannelsQuantity):

            if self.deviceName.__contains__('L783'):
                adcCountsToVolts = 5.12 / 2048.0
                adcOffset = 0
                adcScale = 1
            elif self.deviceName.__contains__('E2010'):
                adcCountsToVolts = 3.31776 / 8192.0
                adcOffset = self.adcOffset[chan + indexOfADCInputRange * self.realChannelsQuantity]
                adcScale = self.adcScale[chan + indexOfADCInputRange * self.realChannelsQuantity]
            else:
                adcCountsToVolts = 1
                adcOffset = 0
                adcScale = 1


            self.callingObj.dataIn.append(np.reshape((self.adcData[::, chan:chan+1]  + adcOffset) * adcScale*adcCountsToVolts/ self.chanAdcGain[chan], self.realCadresQuantity))

            self.callingObj.dataInLabels.append(self.filename+'_ch#'+str(self.chanAdcOrdinal[chan]))

            self.callingObj.dti.append(np.power(self.channelRate*1000.0, -1))
            self.callingObj.frq.append(int(round(self.channelRate * 1000.0)))




