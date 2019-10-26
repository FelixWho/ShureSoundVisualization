import scipy.io.wavfile
import numpy as np

from fft import fft

rate, data = scipy.io.wavfile.read('test/piano50.wav')
data = data[:,0]
t = np.linspace(0,len(data)/rate,len(data))

fft.sigFreq(t, rate, data)