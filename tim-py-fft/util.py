import numpy
import numpy as np
from scipy import fftpack
# import matplotlib.pyplot as plt

class util():
    '''
    @param: rate The sampling rate of the input audio;
    @param: x The discrete magnitude function over time;
    @param: plot Whether or not to show the plot of the ttf.
    
    @return: A The function of magnitude for each frequency;
    @return: freq The reference of frequency relating to A.
    '''

    @staticmethod
    def FFT(rate, x, display=False):
        l_x = len(x)
        t = np.linspace(0,l_x/rate,l_x)

        # if display:
        #     fig, ax = plt.subplots()

        #     ax.plot(t, x)

        #     ax.set_title("Signal Amplitude over Time")
        #     ax.set_xlabel("Time [s]")
        #     ax.set_ylabel("Signal amplitude")

        A = fftpack.fft(x)
        freq = fftpack.fftfreq(l_x) * rate

        # if display:

        #     fig, ax = plt.subplots()

        #     ax.stem(freq, np.abs(A), use_line_collection=True)

        #     ax.set_title("Amplitude of Sine Functions of Different Frequencies")
        #     ax.set_xlabel('Frequency in Hertz [Hz]')
        #     ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')

        #     ax.set_xlim(0, 20000)

        #     plt.show()

        return abs(A), freq

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

        # if display:
        #     fig, ax = plt.subplots()
        #     ax.plot(t, x, "b")

        #     peak_tmp = []
        #     for i in range(0,l_x):
        #         if i in peak: 
        #             peak_tmp.append(x[i])
        #         else: 
        #             peak_tmp.append(0)

        #     ax.stem(t, peak_tmp, "g")
            
        #     ax.set_title("Peaks of the Sound Wave")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude')

        #     plt.show()

        return peak

    '''
    @param: rate The sampling rate of the input audio;
    @param: x The discrete magnitude function over time;
    @param: display Whether or not to show the plot of the peaks.

    @return: peak The list of position of peaks.
    '''
    @staticmethod
    def findSteepRaisingEdge(rate, x, display=False): 
        # note because of the property of the wave form, it is actually hard to use the Z-Score test to find major peaks
        # instead, it is a good way yo find major raises (the steep raising edges)

        l_window = 25
        thd = 2.5

        s1 = 0
        s2 = 0
        ss1 = []
        ss2 = []
        sss = []
        sig = []
        l_x = len(x)
        peak = []

        for i in range(0, l_window):
            s1 += x[i];
            s2 += x[i] ** 2

            ss1.append(0)
            ss2.append(0)
            sig.append(0)
            sss.append(0)

        for i in range(l_window, l_x):
            sigma = (s2/l_window-(s1/l_window)**2) ** 0.5
            sig.append(sigma)

            if x[i] > s1/l_window + thd * sigma: peak.append(i)
                # if ((i>0 and x[i-1]<x[i]) or i==0) and ((i<l_x-1 and x[i]>x[i+1]) or i==l_x-1): peak.append(i)
            s1 = s1 - x[i-l_window] + x[i]
            s2 = s2 - x[i-l_window] ** 2 + x[i] ** 2

            sss.append(s1/l_window)
            ss1.append(s1/l_window + thd * sigma)
            ss2.append(s2/l_window - thd * sigma)

        # if display:
        #     # print(len(peak))
        #     # print(peak)

        #     t = np.linspace(0,l_x/rate,l_x)

        #     fig, ax = plt.subplots()
        #     ax.plot(t, x, 'b')

        #     peak_tmp = []
        #     for i in range(0,l_x):
        #         if i in peak: 
        #             peak_tmp.append(x[i])
        #         else: 
        #             peak_tmp.append(0)

        #     ax.stem(t, np.array(peak_tmp), 'g')

        #     # ax.plot(t,ss1)
        #     # ax.plot(t,ss2)
        #     # ax.plot(t,sig)
        #     # ax.plot(t,sss)
        
        #     ax.set_title("Steep Raising Edges of the Sound Wave")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude')

        #     plt.show()

        return peak

    '''
    @param rate The sampling rate of the audio
    @param x The sequence that is being smoothed
    @param level The number of nodes in the neighbourhood that is used to smooth the data
    @param display Whether or not to display the smoothed curve

    @return y The smoothed data of x
    '''
    @staticmethod
    def smoothAverage(rate, x, level, display=False):
        l_x = len(x)
        y = [0] * l_x

        tmp = 0
        r = level//2
        for i in range(0,level):
            tmp += x[i]

        for i in range(0,r):
            y[i] = tmp/level

        for i in range(r,l_x-r):
            tmp = tmp - x[i-r] + x[i+r]
            y[i] = tmp/level

        for i in range(l_x-r,l_x):
            y[i] = tmp/level


        # if display: 
        #     t = np.linspace(0,l_x/rate,l_x)
        #     fig, ax = plt.subplots()
        #     ax.plot(t,y)

        #     ax.set_title("Smoothed Curve of the Sound Wave (Neighbourhood Average)")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude')

        #     plt.show()

        return y

    '''
    @param rate The sampling rate of the audio
    @param x The sequence that is being smoothed
    @param level The number of frequencies that wanted to preserve
    @param display Whether or not to display the smoothed curve
    
    @return y The smoothed data of x
    '''
    @staticmethod
    def smoothIFFT(rate, x, level, display=False):
        l_x = len(x)

        # A, freq = util.FFT(x)
        # A, freq = sorted([(A[i],freq[i]) for i in range(len(A))], key=lambda x: x[i], reverse=True)[0:len(A)//100*level]
        
        A = np.fft.fft(x)
        tmp = abs(sorted(A, key=lambda x: abs(x), reverse=True)[level])
        
        B = []

        for i in A:
            if abs(i)<abs(tmp):
                B.append(0)
            else:
                B.append(i)

        y = np.fft.ifft(B)

        # if display: 
        #     t = np.linspace(0,l_x/rate,l_x)
        #     fig, ax = plt.subplots()
        #     ax.plot(t,y)
            
        #     ax.set_title("Smoothed Curve of the Sound Wave (FFT and Inversed FFT)")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude')

        #     plt.show()

        return abs(y)


    '''
    @param: x The sequence that is being assessed
    @param: level The level of smooth when assessing

    @return: dev The total deviation of the sound sequence
    '''
    @staticmethod
    def smoothnessAssessAverage(rate, x, level):
        max_x = 0
        for i in x:
            if i > max_x: max_x = i

        y = util.smoothAverage(rate, x,level)

        dev = 0
        tot = 0
        l_x = len(x)
        for i in range(0,l_x):
            dev += (x[i]-y[i])**2
            tot += x[i] ** 2

        return abs(dev/tot)

    '''
    @param: x The sequence that is being assessed
    @param: level The level of smooth when assessing
    
    @return: dev The total deviation of the sound sequence
    '''
    @staticmethod
    def smoothnessAssessIFFT(rate, x, level):
        max_x = 0
        for i in x:
            if i > max_x: max_x = i

        y = util.smoothIFFT(rate, x,level)

        dev = 0
        tot = 0
        l_x = len(x)
        for i in range(0,l_x):
            dev += (x[i]-y[i])**2
            tot += x[i]**2

        return abs(dev/tot)

    '''
    @param: rate The sampling rate of the input audio;
    @param: src The source of the audio that is compared to;
    @param: det The sequence of the audio that is compared.
    
    @return: min_pos The starting position of the best fit of det in src;
    @return: min_dev The total absolute deviation of the best fit
    @return: the function of deviation between det and src over time (relative to the starting position pos).
    '''
    @staticmethod
    def match(rate, src, det, peakPrune=False, display=False):
        peak_src = util.findPeak(rate, src, display=False)
        peak_det = util.findPeak(rate, det, display=False)

        # det = util.smooth(det,5)
        # peak_det = util.findPeak(rate, det, display=True)

        l_src = len(src)
        l_det = len(det)

        lp_src = len(peak_src)
        lp_det = len(peak_det)

        EPSILON = 50

        min_dev = 0x7fffffff
        min_pos = 0
        min_maxsrc = 0
        min_maxdet = 0


        max_det = 0
        for j in range(0,lp_det):
            if max_det < det[peak_det[j]]: max_det = det[peak_det[j]]

        for i in range(0,lp_src):
            if peak_src[i] < peak_det[0]: continue;
            if peak_src[i] - peak_det[0] + l_det > l_src: break;

            # # matching the peaks
            if peakPrune:
                mth = True
                for j in range(1,lp_det):
                    if abs(abs(peak_src[i+j]-peak_src[i])-abs(peak_det[j]-peak_det[0])) > EPSILON:
                        mth = False
                        break

                if not mth: continue

            # after peaks are matched, compare the min total deviation
            tmp_dev = 0
            mth_pos = peak_src[i]-peak_det[0]
            
            max_src = 0
            j=i
            while(peak_src[j]>=mth_pos and j>=0): 
                if max_src < src[peak_src[j]]: max_src = src[peak_src[j]]
                j -= 1
            j=i
            while(peak_src[j]<=mth_pos + l_det and j<lp_src):
                if max_src < src[peak_src[j]]: max_src = src[peak_src[j]]
                j += 1

            for j in range(0,l_det):
                tmp_dev += abs(src[j + mth_pos]/max_src - det[j]/max_det)
                # tmp_dev += abs(src[j + mth_pos] - det[j])

            # print(str(peak_src[i]) + " " + str(max_src) + " " + str(max_det))

            if tmp_dev < min_dev:
                min_dev = tmp_dev
                min_pos = mth_pos
                min_maxsrc = max_src
                min_maxdet = max_det

        dev = []
        for i in range(0,l_det):
            # dev.append(src[i + min_pos] - det[i])
            dev.append(src[i + min_pos]/min_maxsrc - det[i]/min_maxdet)

        # if display:
        #     print(min_pos)
        #     print(min_dev)

        #     t = np.linspace(0,l_det/rate,l_det)

        #     fig, ax = plt.subplots()
        #     ax.plot(t, dev)

        #     ax.set_title("The Deviation Curve of the Best Match of the Curve")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude Difference')

        #     plt.show()

        #     fig, ax = plt.subplots()
        #     ax.plot(t, det / max_det, "b")
        #     ax.plot(t, src[min_pos:min_pos+l_det] / max_src, "g")


        #     ax.set_title("Best Match of the Curve on Original Sound Track")
        #     ax.set_xlabel('Time [s]')
        #     ax.set_ylabel('Signal amplitude')

        #     plt.show()

        return min_pos, min_dev, dev

    