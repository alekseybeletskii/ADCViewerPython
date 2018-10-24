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

# import nnresample
from scipy import signal
import resampy # resampy uses sinc filter that has linear phase response
# all frequency components of the input signal are shifted in time (usually delayed)
# by the same constant amount (the slope of the linear function)
import  numpy as np
class DataResample:
    def __init__(self, callingObj):
        self.callingObj = callingObj

    # def downSampleResampy(self,newSampleRateHz):
    #     for i in range(len(self.callingObj.dataIn)):
    #         # self.callingObj.dataIn[i] = nnresample.resample( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
    #         # self.callingObj.dataIn[i] = signal.resample_poly( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
    #         self.callingObj.dataIn[i] = resampy.resample( self.callingObj.dataIn[i], self.callingObj.frq[i], newSampleRateHz)
    #         self.callingObj.frq[i] = newSampleRateHz
    #         self.callingObj.dti[i] = np.double(1.0/newSampleRateHz)

    def downSampleDecimate(self, dataIn, dataIn_frqHz, target_frqHz):
        #will  be no phase shift !
        decimation_ratio = int(np.round(dataIn_frqHz/ target_frqHz))
        return signal.decimate( dataIn, decimation_ratio, zero_phase=True)

    # def downSampleDecimate(self,target_frqHz):
    #     #will  be no phase shift !
    #     for i in range(len(self.callingObj.dataIn)):
    #         decimation_ratio = int(np.round(self.callingObj.frq[i]/ target_frqHz))
    #         self.callingObj.dataIn[i] = signal.decimate( self.callingObj.dataIn[i], decimation_ratio, zero_phase=True)
    #         self.callingObj.frq[i] = target_frqHz
    #         self.callingObj.dti[i] = np.double(1.0/target_frqHz)
