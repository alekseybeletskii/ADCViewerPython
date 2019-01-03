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
class DataLimits:
    dataLimits = {}

    @classmethod
    def getDataLimitsIndexes(cls, axisIn, x, dataLength):
        cls.dataLimits = {}
        if type(x) is not np.ndarray :
            cls.dataLimits["minIndex"] = int(round(axisIn.range[0] / x))
            cls.dataLimits["maxIndex"] = int(round(axisIn.range[1] / x))
        elif type(x) is np.ndarray:
            i = 0
            while i < x.size:
                if x[i] > axisIn.range[0]:
                   cls.dataLimits["minIndex"] = i
                   break
                i+=1
            i = len(x)-1
            while i > 0:
                if x[i] < axisIn.range[1]:
                   cls.dataLimits["maxIndex"] = i
                   break
                i-=1

        #print('axis range: {}'.format(axIn.range))  # <------- get range of x axis
        #print('data indexes: {}'.format(cls.dataLimits))  # <------- get range of x axis

        cls.dataLimits["minIndex"] = cls.dataLimits.get("minIndex") if cls.dataLimits.get("minIndex") > 0 else 0
        cls.dataLimits["maxIndex"] = cls.dataLimits.get("maxIndex") if cls.dataLimits.get(
            "maxIndex") < dataLength else dataLength

        return cls.dataLimits
