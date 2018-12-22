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

import seaborn
import numpy as np
class ColorPalette:
    colorPalette = []

    @classmethod
    def getColorPalette(cls, paletteSize=10):
        cls.colorPalette.clear()
        size = 1
        HSV_tuples = []
        # HSV_tuples = [(x * 1.0 / N, 1, 1) for x in range(N)]
        hex_out = []
        repeatColors = int(np.ceil(size / paletteSize)) if np.ceil(size / paletteSize) >= 1 else 1
        for i in range(repeatColors):
            # HSV_tuples.extend(seaborn.husl_palette(n_colors=N, h=.003, s=1-0.3*i if i <3 else 1, l=.65))
            HSV_tuples.extend(seaborn.husl_palette(n_colors=paletteSize, h=.003, s=1, l=0.5))
            # HSV_tuples.extend(seaborn.color_palette("Paired", 10))
            # HSV_tuples.extend(seaborn.color_palette("bright", 10))
        for rgb in HSV_tuples:
            rgb = map(lambda x: int(x * 255), rgb)
            #convet to hex string
            cls.colorPalette.append('#%02x%02x%02x' % tuple(rgb))
        return cls.colorPalette


