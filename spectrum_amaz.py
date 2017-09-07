import cross_correlation1_1
import deconv_Bobr
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft

station1, component1, station2, component2, bandpass_down, bandpass_up, traces1, traces1_norm, traces2, traces2_norm,\
time_events = cross_correlation1_1.importing()
corr_array, corr_array_env, half_x_axis, env_corr_max, env_corr_max_sec =\
    cross_correlation1_1.calculations(traces1,traces1_norm, traces2, traces2_norm, time_events)
corr_deconv_array, corr_deconv_array_env, half_x_axis, env_decon_max, env_decon_max_sec = \
    deconv_Bobr.calculations(traces1, traces1_norm, traces2, traces2_norm, time_events)

start_amaz = 13500+192
end_amaz = start_amaz+500
corr_array_amaz = corr_array[:, start_amaz:end_amaz]
corr_deconv_array_amaz = corr_deconv_array[:, start_amaz:end_amaz]
fs = 500

def signal_fft(signal, fs):
    signal_f = fft(signal)  # Raw Fourier transformed signal
    signal_ff = 2.0 / len(signal) * np.abs(signal_f[0:int(len(signal)/2)])  # Fourier transformed signal for plot

    tuple_signal = (signal_f, signal_ff)
    return tuple_signal

print(len(corr_array_amaz[0]))

corr_array_amaz_f = np.empty([len(corr_array_amaz), len(corr_array_amaz[0])])
corr_array_amaz_ff = np.empty([len(corr_array_amaz), int(len(corr_array_amaz[0]) / 2)])
corr_deconv_array_amaz_f = np.empty([len(corr_array_amaz), len(corr_array_amaz[0])])
corr_deconv_array_amaz_ff = np.empty([len(corr_array_amaz), int(len(corr_array_amaz[0]) / 2)])
freqs = np.linspace((1 / fs),  1.0/(2.0 * (1/fs)), len(corr_array_amaz[0]) / 2)

for i in range(len(corr_array_amaz)):
    corr_array_amaz_f[i,:], corr_array_amaz_ff[i,:] = signal_fft(corr_array_amaz[i,:], fs)
    corr_deconv_array_amaz_f[i,:], corr_deconv_array_amaz_ff[i,:] = signal_fft(corr_deconv_array_amaz[i,:], fs)
print('freqs:', len(freqs))
print('amaz: ', len(corr_array_amaz_ff[0]))

mult_factor = 5
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(0, len(corr_array_amaz_ff), 2):
    ax.plot(freqs, corr_array_amaz_ff[i,:] / np.max(corr_array_amaz_ff[i,:]) * mult_factor + time_events[i], c='b',
            label='Cross-correlation')
    ax.plot(freqs, corr_deconv_array_amaz_ff[i,:] / np.max(corr_deconv_array_amaz_ff[i,:]) * mult_factor +
            time_events[i], c='g', label='Deconvolution')

plt.xlabel('Frequency [Hz]')
plt.ylabel('Days')
plt.title('Cross-correlation and deconvolution spectra for selected time period')
handles, labels = ax.get_legend_handles_labels()
handles = handles[0:2]
labels = labels[0:2]
leg = plt.legend(handles, labels)
if leg:
    leg.draggable()
plt.tight_layout()
plt.show()

print(time_events[188])

'''
start_amaz2 = 13000 + 192
end_amaz2 = start_amaz2 + 2000
corr_array_amaz_ex = corr_array[188, start_amaz2:end_amaz2]
corr_deconv_array_amaz_ex = corr_deconv_array[188, start_amaz2:end_amaz2]
np.savetxt('export1.dat', np.c_[corr_array_amaz_ex, corr_deconv_array_amaz_ex], delimiter='\t',
           header='Cross-correlation\tDeconvolution')
'''