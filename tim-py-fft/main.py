import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

from util import util

# --------------------------------------------------------------- full audio
# loading the full audio sequence
rate, data_seq = scipy.io.wavfile.read("test/pianoFull.wav")
data_seq = data_seq[:,0]
l_seq = len(data_seq)

# peek detection for the full audio sequence
peak_seq = util.findPeak(data_seq, display=False)

# ---------------------------------------------------------------- detected sequence
# loading the received audio chunk
rate, data_chunk = scipy.io.wavfile.read('test/piano50.wav')
data_chunk = data_chunk[:,0]
l_chunk = len(data_chunk)

# peek detection for the recorded audio sequence
peak_chunk = util.findPeak(rate, data_chunk, display=False)

# plotting the wave figure and the Fourier Transformation figure
X, freqs = util.ttf(rate, data_chunk, plot=False)

# match_pos = util.match(rate, peak_seq, peak_chunk)

# # brutal forcing the optimal match difference
# min_diff = 0x7fffffff;
# for i in range(0, l_seq-l_chunk, 10):
# 	tmp = 0
# 	for j in range (0, l_chunk, 10):
# 		tmp += abs(data_seq[i+j]-data_chunk[j])
# 	if (tmp < min_diff): min_diff = tmp;

# print(min_diff);
