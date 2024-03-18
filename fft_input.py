#%%

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

fs=44100
duration = 1  # seconds
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

# time domain plot
# plt.subplot(122)
# plt.plot(t, np.fft.ifft(X), 'r')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.tight_layout()
# plt.show()

#try finding the median (so outliers don't skew average)
#the lowesst value above the average is the baseline - search the next 100Hz for the peak

mag = np.abs(X)
average = np.max(mag) / 3
plt.plot(freq, np.full(np.shape(freq), average))

threshold = mag[0:1001] > average

plt.subplot(122)
plt.stem(freq[0:1001], threshold)
plt.tight_layout()
plt.show()

# while(True):
#     fs=44100
#     duration = .5  # seconds
#     print ("Recording Audio")
#     myrecording = sd.rec((int)(duration * fs), samplerate=fs, channels=2,dtype='float64')
#     sd.wait()

#     channel0 = myrecording[:, 0]
#     sample_size_time = len(channel0)
#     t = np.linspace(0, duration, sample_size_time)


#     X = np.fft.fft(channel0)

#     mag = (np.abs(X))[0:1001]
#     average = np.max(mag) / 3

#     print(mag[mag > average][0])

#in the range 100-900 Hz

# %%
