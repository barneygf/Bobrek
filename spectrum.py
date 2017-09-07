import os
from obspy import read
from obspy.signal import freqattributes as freq
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np

path_begin = '01.2010_ML1.2_Z-600\\'  # Path to folder with .seed files

for root, dirs, files in os.walk(path_begin):
    a = files  # Get list of files (in this case - seeds) in folder

print('SEED files: ', a)

traces = read(path_begin + a[0])  # Read Traces from first file. In the loop below Traces from files are attached
    # to Stream, so it is necessary to read first file here.

for i in range(1, len(a)):
    traces += read(path_begin + a[i])  # Read succesive files

#print(traces.__str__(extended=True))  # Print all Traces in Stream

station = 'S015'

bandpass_down = 1.0
bandpass_up = 50.0

tracesZ = traces.select(station=station, component='Z')  # Select Traces from one seismometer and one component

print(tracesZ[109].stats.sampling_rate)

#tracesZ.filter(type='bandpass', freqmin=bandpass_down, freqmax=bandpass_up)

event = 109
dt = 1/tracesZ[event].stats.sampling_rate
y = tracesZ[event].data - np.mean(tracesZ[event].data)
yf = fft(y)
tf = np.linspace(dt, 1.0/(2.0*dt), len(tracesZ[event].data)/2)
yff = 2.0/len(tracesZ[event].data) * np.abs(yf[0:int(len(tracesZ[event].data)/2)])

print(tracesZ[109].stats)

plt.plot(tf, yff/max(yff))
plt.xlabel('Frequency [Hz]')
plt.ylabel('|Y(f)|')
plt.title('Spectrum of event which started at ' + str(tracesZ[event].stats.starttime))
plt.show()