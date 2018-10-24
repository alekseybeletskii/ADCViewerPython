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


from scipy.signal import savgol_filter
from scipy.signal import butter, sosfiltfilt

class DataFilters:
    def __init__(self, callingObj):

        self.callingObj = callingObj

    def subtractSGFilter(self):
        for i in range(len(self.callingObj.dataIn)):
            smoothed = self.savitzky_golay_filt(self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight], self.callingObj.settings["sgFilterWindow"],self.callingObj.settings["sgFilterPolyOrder"])
            self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] = self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] - smoothed

    def replaceWithSGFilter(self):
        for i in range(len(self.callingObj.dataIn)):
            smoothed = self.savitzky_golay_filt(self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight], self.callingObj.settings["sgFilterWindow"],self.callingObj.settings["sgFilterPolyOrder"])
            self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] =  smoothed

    def savitzky_golay_filt(self,data, window_length=1001, polyorder=0, deriv=0, delta=1.0, axis=-1, mode='interp'):
        return savgol_filter(data,window_length,polyorder,mode=mode)


    def butter_bandpass(self, lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            sos = butter(order, [low, high], analog=False, btype='band', output='sos')
            return sos

    def butterworthBandpassZeroPhase(self, data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        filtered = sosfiltfilt(sos, data)
        return filtered