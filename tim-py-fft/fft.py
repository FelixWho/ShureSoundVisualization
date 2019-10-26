import numpy
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

class fft():
	'''
	@param: x The discrete magnitude over time 
	'''
	def sigFreq(t, rate, x, plot=False):
		fig, ax = plt.subplots()

		ax.plot(t, x)
		ax.set_xlabel("Time [s]")
		ax.set_ylabel("Signal amplitude")

		X = fftpack.fft(x)
		freqs = fftpack.fftfreq(len(x)) * rate

		fig, ax = plt.subplots()

		ax.stem(freqs, np.abs(X), use_line_collection=True)
		ax.set_xlabel('Frequency in Hertz [Hz]')
		ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
		ax.set_xlim(0, 20000)

		plt.show()