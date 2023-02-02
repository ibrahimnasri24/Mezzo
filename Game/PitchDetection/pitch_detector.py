import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from os import sep
import time
import pyaudio


def differenceFunction_scipy(x, N, tau_max):
    """
    Compute difference function of data x. This corresponds to equation (6) in [1]

    Faster implementation of the difference function.
    The required calculation can be easily evaluated by Autocorrelation function or similarly by convolution.
    Wiener–Khinchin theorem allows computing the autocorrelation with two Fast Fourier transforms (FFT), with time complexity O(n log n).
    This function use an accellerated convolution function fftconvolve from Scipy package.

    :param x: audio data
    :param N: length of data
    :param tau_max: integration window size
    :return: difference function
    :rtype: list
    """
    x = np.array(x, np.float64)
    w = x.size
    x_cumsum = np.concatenate((np.array([0]), (x * x).cumsum()))
    conv = fftconvolve(x, x[::-1])
    tmp = x_cumsum[w:0:-1] + x_cumsum[w] - x_cumsum[:w] - 2 * conv[w - 1:]
    return tmp[:tau_max + 1]




def differenceFunction(x, N, tau_max):
    """
    Compute difference function of data x. This corresponds to equation (6) in [1]

    Fastest implementation. Use the same approach than differenceFunction_scipy.
    This solution is implemented directly with Numpy fft.


    :param x: audio data
    :param N: length of data
    :param tau_max: integration window size
    :return: difference function
    :rtype: list
    """

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
    """
    Compute cumulative mean normalized difference function (CMND).

    This corresponds to equation (8) in [1]

    :param df: Difference function
    :param N: length of data
    :return: cumulative mean normalized difference function
    :rtype: list
    """

    cmndf = df[1:] * range(1, N) / np.cumsum(df[1:]).astype(float) #scipy method
    return np.insert(cmndf, 0, 1)



def getPitch(cmdf, tau_min, tau_max, harmo_th=0.1):
    """
    Return fundamental period of a frame based on CMND function.

    :param cmdf: Cumulative Mean Normalized Difference function
    :param tau_min: minimum period for speech
    :param tau_max: maximum period for speech
    :param harmo_th: harmonicity threshold to determine if it is necessary to compute pitch frequency
    :return: fundamental period if there is values under threshold, 0 otherwise
    :rtype: float
    """
    tau = tau_min
    while tau < tau_max:
        if cmdf[tau] < harmo_th:
            while tau + 1 < tau_max and cmdf[tau + 1] < cmdf[tau]:
                tau += 1
            return tau
        tau += 1

    return 0    # if unvoiced


def my_compute(chunk, sr, chunk_size=512, f0_min=50, f0_max=500, harmo_thresh=0.1):
    tau_min = int(sr / f0_max)
    tau_max = int(sr / f0_min)


    #Compute YIN
    df = differenceFunction(chunk, chunk_size, tau_max)
    cmdf = cumulativeMeanNormalizedDifferenceFunction(df, tau_max)
    p = getPitch(cmdf, tau_min, tau_max, harmo_thresh)

    pitch=0
    argmin=0

    #Get results
    if np.argmin(cmdf)>tau_min:
        argmin = float(sr / np.argmin(cmdf))
    if p != 0: # A pitch was found
        pitch = float(sr / p)
        harmonic_rate = cmdf[p]
    else: # No pitch, but we compute a value of the harmonic rate
        harmonic_rate = min(cmdf)

    return pitch, harmonic_rate, argmin

def main(pitch_array):
    # Set the parameters for the audio recording
    CHUNK = 1024  # number of audio frames per buffer
    FORMAT = pyaudio.paInt16  # the audio format
    CHANNELS = 1  # number of channels
    RATE = 44100  # the sampling rate

    # Initialize the PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream for audio input
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)

        # Convert the audio data to a numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        pitch, harmonic_rate, argmin = my_compute(audio_data, RATE, chunk_size=CHUNK)
        pitch_array[0] = pitch