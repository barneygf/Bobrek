import cross_correlation1_1
import deconv_Bobr
import matplotlib.pyplot as plt
import numpy as np

station1, component1, station2, component2, bandpass_down, bandpass_up, traces1, traces1_norm, traces2, traces2_norm,\
time_events = cross_correlation1_1.importing()
corr_array, corr_array_env, half_x_axis, env_corr_max, env_corr_max_sec =\
    cross_correlation1_1.calculations(traces1,traces1_norm, traces2, traces2_norm, time_events)
corr_deconv_array, corr_deconv_array_env, half_x_axis, env_decon_max, env_decon_max_sec = \
    deconv_Bobr.calculations(traces1, traces1_norm, traces2, traces2_norm, time_events)

mult_factor = 1  # Multiplication factor for traces amplitude on the plot
plot_distance = 0.75  # Factor of distance between traces on the plot
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(0, len(traces1_norm), 2):
    ax.plot((corr_array[i,:] / max(corr_array[i,:])) * mult_factor + time_events[i], label='Cross-correlation', c='b')
    ax.plot((corr_deconv_array[i, :] / max(corr_deconv_array[i, :])) * mult_factor + time_events[i], c='g',
            label='Deconvolution')  # Plot of traces
    #ax.plot((corr_array_env[i, :] / max(corr_array[i, :])) * mult_factor + time_events[i], c='b', label='Correlation')
    #    # Plot of envelopes
    #ax.plot((corr_deconv_array_env[i, :] / max(corr_deconv_array[i, :])) * mult_factor + time_events[i], c='g',
    #         label='Deconvolution')

ax.scatter(env_corr_max + half_x_axis, time_events, c='r')
ax.scatter(env_decon_max + half_x_axis, time_events, c='b')

x_ticks = np.arange(192, 16193, 500)  # Ticks in miliseconds
my_x_ticks = np.arange(-16, 17)  # New ticks in seconds, and with zero in the middle

plt.xlim(0, len(corr_array[0]))
plt.ylim(time_events[0] - 1, time_events[-1] + 1)
# plt.ylim(-plot_distance, plot_distance * len(corr_array) + plot_distance)
# plt.ylim(-0.2, (plot_distance * len(traces1_norm))/r + 2/dividing_factor)
plt.xlabel('Time [s]')
plt.ylabel('Days')
plt.xticks(x_ticks, my_x_ticks)
plt.title('Cross-correlated and deconvolved traces for stations ' + station1 + ' (component ' + component1 + ')' +
          ' and ' + station2 + ' (component ' + component2 + ')' + '\nBandpass ' + str(bandpass_down) + ' - ' +
          str(bandpass_up) + ' Hz')
plt.grid()
plt.tight_layout()
handles, labels = ax.get_legend_handles_labels()
handles = handles[0:2]
labels = labels[0:2]
leg = plt.legend(handles, labels)
if leg:
    leg.draggable()
plt.show()