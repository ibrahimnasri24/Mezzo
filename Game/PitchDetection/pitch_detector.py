import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from os import sep
import pyaudio

F0_MIN = 75
F0_MAX = 410


def differenceFunction_scipy(x, N, tau_max):
    x = np.array(x, np.float64)
    w = x.size
    x_cumsum = np.concatenate((np.array([0]), (x * x).cumsum()))
    conv = fftconvolve(x, x[::-1])
    tmp = x_cumsum[w:0:-1] + x_cumsum[w] - x_cumsum[:w] - 2 * conv[w - 1:]
    return tmp[:tau_max + 1]




def differenceFunction(x, N, tau_max):
    x = np.array(x, np.float64)
    w = x.size
    tau_max = min(tau_max, w)
    x_cumsum = np.concatenate((np.array([0.]), (x * x).cumsum()))
    size = w + tau_max
    p2 = (size // 32).bit_length()
    nice_numbers = (16, 18, 20, 24, 25, 27, 30, 32)
    size_pad = min(x * 2 ** p2 for x in nice_numbers if x * 2 ** p2 >= size)
    fc = np.fft.rfft(x, size_pad)
    conv = np.fft.irfft(fc * fc.conjugate())[:tau_max]
    return x_cumsum[w:w - tau_max:-1] + x_cumsum[w] - x_cumsum[:tau_max] - 2 * conv



def cumulativeMeanNormalizedDifferenceFunction(df, N):
    cmndf = df[1:] * range(1, N) / np.cumsum(df[1:]).astype(float) #scipy method
    return np.insert(cmndf, 0, 1)



def getPitch(cmdf, tau_min, tau_max, harmo_th=0.1):
    tau = tau_min
    while tau < tau_max:
        if cmdf[tau] < harmo_th:
            while tau + 1 < tau_max and cmdf[tau + 1] < cmdf[tau]:
                tau += 1
            return tau
        tau += 1

    return 0    # if unvoiced


def my_compute(chunk, sr, chunk_size=512, f0_min=75, f0_max=410, harmo_thresh=0.1):
    tau_min = int(sr / f0_max)
    tau_max = int(sr / f0_min)

    df = differenceFunction(chunk, chunk_size, tau_max)
    cmdf = cumulativeMeanNormalizedDifferenceFunction(df, tau_max)
    p = getPitch(cmdf, tau_min, tau_max, harmo_thresh)

    pitch=0
    argmin=0

    if np.argmin(cmdf)>tau_min:
        argmin = float(sr / np.argmin(cmdf))
    if p != 0:
        pitch = float(sr / p)
        harmonic_rate = cmdf[p]
    else:
        harmonic_rate = min(cmdf)

    return pitch, harmonic_rate, argmin

def main(pitch_array):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    while pitch_array[1] == 1:
        data = stream.read(CHUNK)

        audio_data = np.frombuffer(data, dtype=np.int16)

        pitch, harmonic_rate, argmin = my_compute(audio_data, RATE, chunk_size=CHUNK, f0_min=F0_MIN, f0_max=F0_MAX)
        pitch_array[0] = pitch