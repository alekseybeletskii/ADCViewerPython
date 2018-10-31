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
from os import path


class ImportFromTxt(QtWidgets.QMainWindow):

   def __init__(self,callingObj,  *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.callingObj = callingObj

   def openCsvTxt_dx(self):
        # self.callingObj.clearAllViewer()

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, None, "QFileDialog.getOpenFileNames()", "All Files (*)",
                                                     "All Files (*)", options=options)

        for i in range(len(files)):
            dataTxt = pd.read_csv(files[i], names=['x', 'y'], header=None)
            dataX = dataTxt['x']
            dti = abs(np.double(dataX[len(dataX)-1]-dataX[len(dataX)-2]))
            self.callingObj.dti.append(dti)
            self.callingObj.frq.append(int(round(np.power(dti, -1))))
            self.callingObj.dataIn.append(np.asarray(dataTxt['y']))
            filename_and_ext = path.basename(files[i])
            filename, _ = path.splitext(filename_and_ext)
            self.callingObj.dataInLabels.append(filename)

            #print(type(dataX))

   def  openCsvTxt_fullX(self):
        # self.callingObj.clearAllViewer()

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, None, "QFileDialog.getOpenFileNames()", "All Files (*)",
                                                     "All Files (*)", options=options)

        for i in range(len(files)):
            dataTxt = pd.read_csv(files[i], names=['x', 'y'], header=None)
            dataX = np.asarray(dataTxt['x'])

            #print(type(dataX))
            dti = abs(np.double(dataX[len(dataX) - 1] - dataX[len(dataX) - 2]))
            self.callingObj.frq.append(int(round(np.power(dti, -1))))
            self.callingObj.dti.append(dataX)
            self.callingObj.dataIn.append(np.asarray(dataTxt['y']))
            filename_and_ext = path.basename(files[i])
            filename, _ = path.splitext(filename_and_ext)
            self.callingObj.dataInLabels.append(filename)


