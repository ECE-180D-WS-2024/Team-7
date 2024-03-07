#%%

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import pygame

fs=44100
duration = .01  # seconds
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
#plt.show()

# testing to print an integer output proportional to the fundamental frequency
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
    
#pygame testing

def get_pos():
    MULT = 10

    fs=44100
    duration = 1  # seconds
    myrecording = sd.rec((int)(duration * fs), samplerate=fs, channels=2,dtype='float64')
    sd.wait()

    channel0 = myrecording[:, 0]
    sample_size_time = len(channel0)

    X = np.fft.fft(channel0)

    mag = (np.abs(X))[0:1001]
    average = np.max(mag) / 2
    x = np.argmax(mag)
    # for i, val in enumerate(mag):
    #     if val > average:
    #         x = i
    #         break
    print(x)

    #earlier testing, ~64 was maximum, so map to screen width
    TEST_MAX = 1000

    mapped = (x * (WINDOW_WIDTH-2*CIRC_RADIUS)/TEST_MAX) + CIRC_RADIUS

    return (int)(mapped)



pygame.init()

#Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
CIRC_RADIUS = 50

#Color definitions
GREEN = (61, 168, 89)
PURPLE = (63, 54, 107)
ORANGE = (161, 119, 21)
BLUE = (0, 0, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #background
    screen.fill(WHITE)

    x = get_pos()

    pygame.draw.circle(screen, GREEN, (x, WINDOW_HEIGHT//2), CIRC_RADIUS)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
# %%
