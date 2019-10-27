import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

from util import util

# --------------------------------------------------------------- source audio
# loading the full audio sequence
rate, data_src = scipy.io.wavfile.read("test/HelloFull.wav")
data_src = data_src[:,0]
l_src = len(data_src)

# ---------------------------------------------------------------- detected sequence
# loading the received audio chunk
rate, data_det = scipy.io.wavfile.read('test/Hello50.wav')
data_det = data_det[:,0]
l_det = len(data_det)

# ---------------------------------------------------------------- demos

# raising edge detection for the recorded audio sequence
raising_det = util.findSteepRaisingEdge(rate, data_det, display=False)

# peak detection for the recorded audio sequence
peak_det = util.findPeak(rate, data_det, display=False)

# Fast Fourier Transmation for the curve
A, freq = util.FFT(rate, data_det, display=False)

# manually make some noice
data_det = data_det + 3 * np.random.randn(len(data_det))

# matching for the smallest total deviation
min_pos, min_dev, dev = util.match(rate, data_src, data_det, peakPrune=True, display=False)

# Smoothing curves

util.smoothAverage(rate, data_det, 50, display=False)
util.smoothIFFT(rate, data_det, 50, display=False)

# Smoothness assessments
print(util.smoothnessAssessAverage(rate, data_det, 10))
print(util.smoothnessAssessIFFT(rate, data_det, 10))

print("Finished.")