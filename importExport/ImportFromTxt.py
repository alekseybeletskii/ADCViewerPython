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
from os import path as ospath
from pyqtgraph import PlotDataItem as plotDataItem
from importExport.DataModel import DataModel


class ImportFromTxt(QtWidgets.QMainWindow):

    def __init__(self, callingObj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainObject = callingObj
        self.allData = []


    def openCsvTxt(self):

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)

        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "open csv(txt) files", self.mainObject.latestFilePath, "All Files (*)",
                                                      "All Files (*)", options=options)
        if files:
            self.mainObject.latestFilePath = ospath.abspath(files[0])

        for i in range(len(files)):
            dataTxt = pd.read_csv(files[i], names=['x', 'y'], header=None)
            time = np.asarray(dataTxt['x'])
            data = np.asarray(dataTxt['y'])
            dti = abs(np.double(time[len(time) - 1] - time[len(time) - 2]))

            filename_and_ext = ospath.basename(files[i])
            filename, _ = ospath.splitext(filename_and_ext)

            adcChannelTimeShift = 0
            adcChannel = 0
            time = np.arange(0, (data.size) * dti, dti) + adcChannelTimeShift
            label = filename + '_ch#' + str(adcChannel)
            pdi = plotDataItem(time, data, name=label)
            dataModel = DataModel(pdi, label,  dti, adcChannel, adcChannelTimeShift)
            dataModifiers = {'timeshift': 0.0, 'datamultiplier': 1.0, 'datashift': 0.0, 'independentvar': i,
                                  'datatype': 'whatever'}
            dataModel.setDataModifiers(dataModifiers)

            self.allData.append(dataModel)


        return self.allData
