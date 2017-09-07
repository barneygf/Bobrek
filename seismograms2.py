from obspy import read
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import os
import numpy as np

path_begin = '01.2010_ML1.2_Z-600\\'  # Path to folder with .seed files

for root, dirs, files in os.walk(path_begin):
    a = files  # Get list of files (in this case - seeds) in folder

print('SEED files: ', a)

traces = read(path_begin + a[0])  # Read Traces from first file. In the loop below Traces from files are attached
    # to Stream, so it is necessary to read first file here.

for i in range(1, len(a)):
    traces += read(path_begin + a[i])  # Read succesive files

print(traces.__str__(extended=True))  # Print all Traces in Stream

station = 'S015'

bandpass_down = 1.0
bandpass_up = 50.0

tracesZ = traces.select(station=station, component='Z')  # Select Traces from one seismometer and one component
#tracesZ.filter(type='bandpass', freqmin=bandpass_down, freqmax=bandpass_up)

tracesZ_norm = tracesZ.copy()
tracesZ_norm.normalize()  # All Traces in the Stream normalized to their respective absolute maximum

tracesZ_globnorm = tracesZ.copy()
tracesZ_globnorm.normalize(global_max=True)

t = np.arange(0, tracesZ[0].stats.npts / tracesZ[0].stats.sampling_rate, tracesZ[0].stats.delta)

plots_distance_norm = 0.2
y_ticks_distance = 10
y_ticks_norm = np.arange(0, len(tracesZ_norm) * plots_distance_norm + 1, y_ticks_distance * plots_distance_norm)
y_ticks_norm_my = np.arange(1, len(tracesZ_norm), y_ticks_distance)

fig1 = plt.figure(1)
ax = fig1.add_subplot(1,1,1)
for i in range(len(tracesZ_norm)):
    ax.plot(t, tracesZ_norm[i].data + plots_distance_norm * i)
#plt.tight_layout()
ax.set_xlim(0, t[-1])
ax.set_ylim(0 - max(tracesZ_norm[0].data), len(tracesZ_norm) * plots_distance_norm)
ax.set_title('Traces normalized to their respective absolute maximum for station ' + station)
ax.set_xlabel('Time [s]')
plt.yticks(y_ticks_norm, y_ticks_norm_my)
ax.set_ylabel('Traces')
fig1.tight_layout()

fig2 = plt.figure(2)
ax = fig2.add_subplot(1,1,1)
for i in range(len(tracesZ_globnorm)):
    ax.plot(t, tracesZ_globnorm[i].data + plots_distance_norm * i)
ax.set_xlim(0, t[-1])
ax.set_ylim(0 - max(tracesZ_globnorm[0].data), len(tracesZ_globnorm) * plots_distance_norm)
ax.set_title('Traces normalized to global absolute maximum for station ' + station)
ax.set_xlabel('Time [s]')
plt.yticks(y_ticks_norm, y_ticks_norm_my)
ax.set_ylabel('Traces')
fig2.tight_layout()

plt.show()