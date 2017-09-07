import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

def noise_cross_deconv(noise_data1, noise_data2, fs=100, sec_out=30):
    data_noise_temp = np.array([noise_data1, noise_data2])
    Nt = data_noise_temp.shape[1]
    Nc = 2 * Nt - 1
    Nfft = 2 ** np.ceil(np.log2(Nc))

    cross_coher_temp = fftpack.fft(data_noise_temp, int(Nfft))
    #print
    #np.abs(cross_coher_temp[1])
    cross_coher_temp = cross_coher_temp[0] * np.conj(cross_coher_temp[1]) / np.abs(cross_coher_temp[0]) / np.abs(cross_coher_temp[0])
    #cross_coher_temp = cross_coher_temp[0] * np.conj(cross_coher_temp[1]) / np.square(np.abs(cross_coher_temp[1]))
    cross_coher_temp = np.real(fftpack.ifft(cross_coher_temp))
    #cross_coher_temp = fftpack.ifft(cross_coher_temp)
    #plt.plot(cross_coher_temp)
    cross_coher_temp = np.concatenate((cross_coher_temp[-Nt + 1:], cross_coher_temp[:Nt + 1]))
    #plt.plot(cross_coher_temp, c='k')
    #plt.show()
    #cross_coher_temp = cross_coher_temp[(len(noise_data1) - sec_out * fs - 1):(len(noise_data1) + sec_out * fs)]
    #cross_coher_temp = cross_coher_temp[(len(noise_data1) - 1):(len(noise_data1))]
    del data_noise_temp
    return cross_coher_temp