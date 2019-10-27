import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

from util import util

# --------------------------------------------------------------- source audio
# loading the full audio sequence
rate, data_src = scipy.io.wavfile.read("test/HelloFull.wav")
data_src = data_src[:,0]
l_src = len(data_src)

# peek detection for the full audio sequence
# peak_src = util.findPeak(rate, data_src, display=False)

# ---------------------------------------------------------------- detected sequence
# loading the received audio chunk
rate, data_seq = scipy.io.wavfile.read('test/Hello50.wav')
data_seq = data_seq[:,0]
l_seq = len(data_seq)

# peek detection for the recorded audio sequence
# peak_src = util.findPeak(rate, data_seq, display=True)


# --------------------------------------------------------------- pattern matching
# plotting the wave figure and the Fourier Transformation figure
# X, freqs = util.ttf(rate, data_seq, plot=True)

# matching for the smallest total deviation

# manually make some noice
data_seq = data_seq + 1 * np.random.randn(l_seq)

min_pos, min_dev, dev = util.match(rate, data_src, data_seq, display=True)