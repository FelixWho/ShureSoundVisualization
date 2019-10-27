import numpy
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

class util():
	'''
	@param: x The discrete magnitude over time 
	'''
	def ttf(rate, x, plot=False):
		l_x = len(x)
		t = np.linspace(0,l_x/rate,l_x)

		if plot:
			fig, ax = plt.subplots()

			ax.plot(t, x)
			ax.set_xlabel("Time [s]")
			ax.set_ylabel("Signal amplitude")

		X = fftpack.fft(x)
		freqs = fftpack.fftfreq(l_x) * rate

		if plot:

			fig, ax = plt.subplots()

			ax.stem(freqs, np.abs(X), use_line_collection=True)
			ax.set_xlabel('Frequency in Hertz [Hz]')
			ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
			ax.set_xlim(0, 20000)

			plt.show()

		return X, freqs

	def findPeak(rate, x, display=False):
		l_x = len(x)
		peak = []
		if x[0]>x[1]: peak.append(0) 
		
		for i in range(1,l_x-1):
			if x[i-1]<=x[i] and x[i]>=x[i+1]: peak.append(i)

		if x[l_x-2] < x[l_x-1]: peak.append(l_x-1)

		t = np.linspace(0,l_x/rate,l_x)

		if display:
			fig, ax = plt.subplots()
			ax.plot(t, x)

			peak_tmp = []
			for i in range(0,l_x):
				if i in peak: 
					peak_tmp.append(x[i])
				else: 
					peak_tmp.append(0)
			ax.stem(t, peak_tmp)
			plt.show()

		return peak

		# l_window = 25
		# thd = 3.5

		# s1 = 0
		# s2 = 0
		# ss1 = []
		# ss2 = []
		# sss = []
		# sig = []
		# l_x = len(x)
		# peak = []

		# for i in range(0, l_window):
		# 	s1 += x[i];
		# 	s2 += x[i] ** 2

		# 	ss1.append(0)
		# 	ss2.append(0)
		# 	sig.append(0)
		# 	sss.append(0)

		# for i in range(l_window, l_x):
		# 	sigma = (s2/l_window-(s1/l_window)**2) ** 0.5
		# 	sig.append(sigma)

		# 	if x[i] > s1/l_window + thd * sigma: peak.append(i)
		# 		# if ((i>0 and x[i-1]<x[i]) or i==0) and ((i<l_x-1 and x[i]>x[i+1]) or i==l_x-1): peak.append(i)
		# 	s1 = s1 - x[i-l_window] + x[i]
		# 	s2 = s2 - x[i-l_window] ** 2 + x[i] ** 2

		# 	sss.append(s1/l_window)
		# 	ss1.append(s1/l_window + thd * sigma)
		# 	ss2.append(s2/l_window - thd * sigma)

		# if display:
		# 	print(len(peak))
		# 	print(peak)

		# rate = 44100
		# t = np.linspace(0,l_x/rate,l_x)

		# fig, ax = plt.subplots()
		# ax.plot(t, x)

		# peak_tmp = []
		# for i in range(0,l_x):
		# 	if i in peak: 
		# 		peak_tmp.append(x[i])
		# 	else: 
		# 		peak_tmp.append(0)
		# ax.stem(t, np.array(peak_tmp))

		# ax.plot(t,ss1)
		# # ax.plot(t,ss2)
		# # ax.plot(t,sig)
		# # ax.plot(t,sss)

		# plt.show()

		# return peak