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
from scipy import signal
import matplotlib.pyplot as plt
import requests
class TestDataGenerator:
    def __init__(self, callingObj):

        self.callingObj = callingObj
    def generatePeriodicAndNoise(self):
        # Create the data
        fs = 1e4
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        time = np.arange(N) / float(fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        # self.matplotlibPlot(carrier+noise, fs, 1024)

        return  carrier + noise, fs

    def generateChirpAndNoise(self):

        fs = 8000
        T = 10
        t = np.linspace(0, T, T * fs, endpoint=False)
        carrier = signal.chirp(t, f0=1500, f1=250, t1=10, method='hyperbolic')
        noise_power = 0.005 * fs / 2
        noise = np.random.normal(scale=np.sqrt(noise_power), size=t.shape)
        noise *= np.exp(-t / 5)

        # self.matplotlibPlot(carrier+noise, fs, 1024)

        return  carrier + noise, fs

    def nightingaleSongSpectr(self):
        from scipy.io import wavfile
        # http://www.orangefreesounds.com/nightingale-sound/
        # https: // www.oreilly.com / library / view / elegant - scipy / 9781491922927 / ch04.html
        # https://github.com/elegant-scipy/elegant-scipy/tree/master/data/nightingale.wav
        fs, audio = wavfile.read('sound/nightingale.wav')
        #fs = 44100 Hz
        #print(' nightingaleSong fs: ', fs)
        # convert to mono by averaging the left and right channels
        audio = np.mean(audio, axis=1)
        # np.save('data/nightingale.npy', audio)
        # self.matplotlibPlot(audio, fs, 1024)
        return  audio, fs


    @staticmethod
    def matplotlibPlot(signalIn, fs, wind):
        f, t, Sxx = signal.spectrogram(signalIn, fs=fs, window='hanning', detrend=False, noverlap=int(wind*0.8), nperseg=wind, nfft=wind)
        plt.pcolormesh(t, f,  10 * np.log10(Sxx), cmap='viridis')
        plt.title('Hyperbolic Chirp, f(0)=1500, f(10)=250')
        plt.xlabel('t (sec)')
        plt.ylabel('Frequency (Hz)')
        plt.grid()
        plt.show()
