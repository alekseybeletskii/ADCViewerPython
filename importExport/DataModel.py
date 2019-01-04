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
class DataModel():

    def __init__(self, plotDataItem, filename, dt=0, adcChannel=0, adcChannelTimeShift=0):
        super(self.__class__, self).__init__()
        self.initSelf(plotDataItem, filename, dt, adcChannel, adcChannelTimeShift)

    def initSelf(self, plotDataItem, filename, dt, adcChannel, adcChannelTimeShift):
        self.plotDataItem = plotDataItem
        self.dt = dt
        self.adcChannel = adcChannel
        self.adcChannelTimeShift = adcChannelTimeShift
        self.dataModifiers = {'timeshift':0.0, 'datamultiplier':1.0, 'datashift':0.0}
        self.fileName = filename
        self.isVisible = False

    def getPlotDataItem(self):
        return self.plotDataItem

    def getDt(self):
        return self.dt

    def getAdcChannel(self):
        return self.adcChannel

    def getAdcChannelTimeShift(self):
        return self.adcChannelTimeShift

    def getFileName(self):
        return self.fileName

    def applyDataModifiers(self):
        x, y = self.plotDataItem.getData()
        x = x + np.double(self.dataModifiers['timeshift'])
        y = np.multiply(y+np.double(self.dataModifiers['datashift']), np.double(self.dataModifiers['datamultiplier']))
        self.plotDataItem.setData(x, y)

    def adcZeroShiftCompensation(self,zeroStartSecond,zeroEndSecond):
        x, y = self.plotDataItem.getData()
        start = zeroStartSecond
        end = zeroEndSecond
        if zeroEndSecond < zeroStartSecond:
            start = zeroEndSecond
            end = zeroStartSecond
        if start < 0 | end < 0 | end < self.dt | end > np.multiply(y.size, self.dt):
            print('enter proper time range')
            return
        startIndex = int(start/self.dt) if int(start/self.dt) < y.size else 0
        endIndex = int(end/self.dt) if int(end/self.dt) < y.size else 0

        # zero = np.divide(y[endIndex]-y[startIndex],endIndex-startIndex)
        y = y - np.average(y[startIndex:endIndex])
        self.plotDataItem.setData(x, y)

    def setVisible(self, isVisible):
        self.isVisible = isVisible

    def isVisible(self):
        return self.isVisible






