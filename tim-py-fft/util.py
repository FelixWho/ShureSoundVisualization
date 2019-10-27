import numpy
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

class util():
	'''
	@param: rate The sampling rate of the input audio;
	@param: x The discrete magnitude function over time;
	@param: plot Whether or not to show the plot of the ttf.
	
	@return: A The function of magnitude for each frequency;
	@return: freq The reference of frequency relating to A.
	'''

	@staticmethod
	def ttf(rate, x, plot=False):
		l_x = len(x)
		t = np.linspace(0,l_x/rate,l_x)

		if plot:
			fig, ax = plt.subplots()

			ax.plot(t, x)
			ax.set_xlabel("Time [s]")
			ax.set_ylabel("Signal amplitude")

		A = fftpack.fft(x)
		freq = fftpack.fftfreq(l_x) * rate

		if plot:

			fig, ax = plt.subplots()

			ax.stem(freq, np.abs(A), use_line_collection=True)
			ax.set_xlabel('Frequency in Hertz [Hz]')
			ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
			ax.set_xlim(0, 20000)

			plt.show()

		return np.abs(A), freq

	'''
	@param: rate The sampling rate of the input audio;
	@param: x The discrete magnitude function over time;
	@param: display Whether or not to show the plot of the peaks.

	@return: peak The list of position of peaks.
	'''
	@staticmethod
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

	'''
	@param: rate The sampling rate of the input audio;
	@param: src The source of the audio that is compared to;
	@param: seq The sequence of the audio that is compared.
	
	@return: min_pos The starting position of the best fit of seq in src;
	@return: min_dev The total absolute deviation of the best fit
	@return: the function of deviation between seq and src over time (relative to the starting position pos).
	'''
	@staticmethod
	def match(rate, src, seq, display=False):
		peak_src = util.findPeak(rate, src, display=False)
		peak_seq = util.findPeak(rate, seq, display=False)

		l_src = len(src)
		l_seq = len(seq)

		lp_src = len(peak_src)
		lp_seq = len(peak_seq)

		EPSILON = 50

		min_dev = 0x7fffffff
		min_pos = 0
		min_maxsrc = 0
		min_maxseq = 0


		max_seq = 0
		for j in range(0,lp_seq):
			if max_seq < seq[peak_seq[j]]: max_seq = seq[peak_seq[j]]

		for i in range(0,lp_src):
			if peak_src[i] < peak_seq[0]: continue;
			if peak_src[i] - peak_seq[0] + l_seq > l_src: break;

			# matching the peaks
			mth = True
			for j in range(1,lp_seq):
				if abs(abs(peak_src[i+j]-peak_src[i])-abs(peak_seq[j]-peak_seq[0])) > EPSILON:
					mth = False
					break

			if not mth: continue

			# after peaks are matched, compare the min total deviation
			tmp_dev = 0
			mth_pos = peak_src[i]-peak_seq[0]
			
			max_src = 0
			j=i
			while(peak_src[j]>=mth_pos and j>=0): 
				if max_src < src[peak_src[j]]: max_src = src[peak_src[j]]
				j -= 1
			j=i
			while(peak_src[j]<=mth_pos + l_seq and j<lp_src):
				if max_src < src[peak_src[j]]: max_src = src[peak_src[j]]
				j += 1

			for j in range(0,l_seq):
				tmp_dev += abs(src[j + mth_pos]/max_src - seq[j]/max_seq)
				# tmp_dev += abs(src[j + mth_pos] - seq[j])

			# print(str(peak_src[i]) + " " + str(max_src) + " " + str(max_seq))

			if tmp_dev < min_dev:
				min_dev = tmp_dev
				min_pos = mth_pos
				min_maxsrc = max_src
				min_maxseq = max_seq

		dev = []
		for i in range(0,l_seq):
			# dev.append(src[i + min_pos] - seq[i])
			dev.append(src[i + min_pos]/min_maxsrc - seq[i]/min_maxseq)

		if display:
			t = np.linspace(0,l_seq/rate,l_seq)
			fig, ax = plt.subplots()
			ax.plot(t, dev)
			plt.show()

			print(min_pos)
			print(min_dev)

		return min_pos, min_dev, dev


	# Z-Score peak Finding
	# def findPeak(rate, x, display=False): 
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