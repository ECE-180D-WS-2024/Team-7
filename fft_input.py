#%%

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

fs=44100
duration = 3  # seconds
print ("Recording Audio")
myrecording = sd.rec((int)(duration * fs), samplerate=fs, channels=2,dtype='float64')
sd.wait()

channel0 = myrecording[:, 0]
sample_size_time = len(channel0)
t = np.linspace(0, duration, sample_size_time)


X = np.fft.fft(channel0)
N = len(X)
n = np.arange(N)
T = N/fs
freq = n/T 

plt.figure(figsize = (12, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 1000)

plt.subplot(122)
plt.plot(t, np.fft.ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

# %%
