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


class ImportFromLGraph(QtWidgets.QMainWindow):

   def __init__(self,callingObj,  *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.callingObj = callingObj

   def openLGraph(self):
        self.callingObj.clearAllViewer()

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        dataFiles, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"ADC binary files", self.callingObj.latestFilePath,"*.dat;;All Files (*)", options=options)

        if dataFiles:
            self.callingObj.latestFilePath = ospath.abspath(dataFiles[0])

        for i in range(len(dataFiles)):
            path_to_dir, filename_and_ext = ospath.split(dataFiles[i])
            filename, _ = ospath.splitext(filename_and_ext)
            self.callingObj.dataInLabels.append(filename)
            parFile = ospath.join(path_to_dir, filename + ".par")



            dataParameters = namedtuple('dataParameters','adcSignature, deviceName, createDateTime')
                                        #                  ', channelsMax,'
                                        # ' realChannelsQuantity, realCadresQuantity, realSamplesQuantity,'
                                        # ' totalTime, adcRate, interCadreDelay, channelRate,'
                                        # ' activeAdcChannelArray, adcChannelArray, adcGainArray,'
                                        # ' isSignalArray, dataFormat, realCadres64, adcScale,'
                                        # ' adcOffset, calibrOffset, calibrScale, segments  '
                                        # )
            with open(parFile, "rb") as binary_parFile:
                # Seek a specific position in the file and read N bytes
                # binary_parFile.seek(0, 0)  # Go to beginning of the file
                # adcSignature = binary_parFile.read(20).decode('utf-8').strip()
                allBytes = binary_parFile.read()
                # dataParameters.adcSignature = str(struct.unpack_from('<20s', allBytes , offset=0)).strip()
                # dataParameters.ActiveAdcChannelArray = struct.unpack_from('<32B', allBytes , offset=95)

                dataParameters._make(struct.unpack_from('20s17s26s', allBytes,  offset=0))






                print(dataParameters)
                # print(str(dataParameters.deviceName))
                # print(str(dataParameters.createDateTime))
            # dataTxt = pd.read_csv(files[i], names=['x', 'y'], header=None)
            # dataX = dataTxt['x']
            # dti = abs(np.double(dataX[len(dataX)-1]-dataX[len(dataX)-2]))
            # self.callingObj.dti.append(dti)
            # self.callingObj.frq.append(int(round(np.power(dti, -1))))
            # self.callingObj.dataIn.append(np.asarray(dataTxt['y']))


            #print(type(dataX))

