import scipy.io.wavfile
import numpy as np

from fft import fft

# loading the received audio chunk
rate, data_chunk = scipy.io.wavfile.read('test/piano50.wav')
data_chunk = data_chunk[:,0]
l_chunk = len(data_chunk)

mean_chunk = 0;
for i in data_chunk:
	mean_chunk += i
mean_chunk /= l_chunk

# loading the original audio sequence
rate, data_seq = scipy.io.wavfile.read("test/pianoFull.wav")
data_seq = data_seq[:,0]
l_seq = len(data_seq)

mean_seq = 0;
for i in data_seq:
	mean_seq += i
mean_seq /= l_seq

# plotting the wave figure and the Fourier Transformation figure
t = np.linspace(0,l_chunk/rate,l_chunk)
X, freqs = fft.sigFreq(t, rate, data_chunk, plot=True)

# brutal forcing the optimal match difference
min_diff = 0x7fffffff;
for i in range(0, l_seq-l_chunk, 10):
	tmp = 0
	for j in range (0, l_chunk, 10):
		tmp += abs(data_seq[i+j]-data_chunk[j])
	if (tmp < min_diff): min_diff = tmp;

print(min_diff);

