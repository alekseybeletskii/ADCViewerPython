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
        self.matplotlibPlot(carrier+noise, fs, 1024)

        return  carrier + noise

    def generateChirpAndNoise(self):

        fs = 8000
        T = 10
        t = np.linspace(0, T, T * fs, endpoint=False)
        carrier = signal.chirp(t, f0=1500, f1=250, t1=10, method='hyperbolic')
        noise_power = 0.005 * fs / 2
        noise = np.random.normal(scale=np.sqrt(noise_power), size=t.shape)
        noise *= np.exp(-t / 5)

        self.matplotlibPlot(carrier+noise, fs, 1024)

        return  carrier + noise

    def nightingaleSongSpectr(self):
        from scipy.io import wavfile
        # https://github.com/elegant-scipy/elegant-scipy/tree/master/data/nightingale.wav
        fs, audio = wavfile.read('sound/nightingale.wav')
        print(' nightingaleSong fs: ', fs)
        # convert to mono by averaging the left and right channels
        audio = np.mean(audio, axis=1)
        # np.save('data/nightingale.npy', audio)
        self.matplotlibPlot(audio, fs, 1024)
        return  audio


    @staticmethod
    def matplotlibPlot(signalIn, fs, wind):
        f, t, Sxx = signal.spectrogram(signalIn, fs=fs, window='hanning', detrend=False, noverlap=int(wind*0.8), nperseg=wind, nfft=wind)
        plt.pcolormesh(t, f,  10 * np.log10(Sxx), cmap='viridis')
        plt.title('Hyperbolic Chirp, f(0)=1500, f(10)=250')
        plt.xlabel('t (sec)')
        plt.ylabel('Frequency (Hz)')
        plt.grid()
        plt.show()
