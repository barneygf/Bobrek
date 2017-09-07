from xcorr_deconv2 import noise_cross_deconv
import def_import_Bobrek
import numpy as np
import matplotlib.pyplot as plt
from obspy.signal.filter import envelope

def importing():
    global station1, component1, station2, component2, bandpass_down, bandpass_up, traces1, traces1_norm, traces2,\
        traces2_norm, time_events
    traces = def_import_Bobrek.import_seeds()
    print(traces.__str__(extended=True))  # Print all Traces in Stream

    station1 = 'S013'  # Choose station 1 for cross correlation
    component1 = 'Z'
    station2 = 'S015'  # Choose station 2 for cross correlation
    component2 = 'Z'
    bandpass_down = None  # Lower cutoff frequency for bandpass filter
    bandpass_up = None  # Upper cutoff frequency for bandpass filter

    traces1 = def_import_Bobrek.select_seeds(input_traces=traces, station=station1, component=component1,
                                             bandpass_down=bandpass_down, bandpass_up=bandpass_up)
    traces1_norm = def_import_Bobrek.select_seeds(input_traces=traces, station=station1, component=component1,
                                                  bandpass_down=bandpass_down, bandpass_up=bandpass_up, norm=True)
    traces2 = def_import_Bobrek.select_seeds(input_traces=traces, station=station2, component=component2,
                                             bandpass_down=bandpass_down, bandpass_up=bandpass_up)
    traces2_norm = def_import_Bobrek.select_seeds(input_traces=traces, station=station2, component=component2,
                                                  bandpass_down=bandpass_down, bandpass_up=bandpass_up, norm=True)

    time_events = def_import_Bobrek.import_time_events()  # Import event's times

    data1 = (station1, component1, station2, component2, bandpass_down, bandpass_up, traces1, traces1_norm, traces2,
             traces2_norm, time_events)
    return data1

def calculations(traces1, traces1_norm, traces2, traces2_norm, time_events):
    global corr_deconv_array, corr_deconv_array_env, half_x_axis, env_max, env_max_sec
    corr_deconv_array = np.empty([len(traces1_norm), 2 * len(traces1_norm[0])])  # Init empty numpy array
    # for calculating deconvolution
    print(corr_deconv_array.shape)
    a = noise_cross_deconv(traces1_norm[0], traces2_norm[0], fs=500)
    print(a.shape)

    for i in range(len(traces1_norm)):
        corr_deconv_array[i,:] = noise_cross_deconv(traces1_norm[i], traces2_norm[i], fs=500)  # Calculating
            # deconvolution

    corr_deconv_array_env = np.empty_like(corr_deconv_array)  # Init empty array with the same shape as another array
    for i in range(len(corr_deconv_array)):
        corr_deconv_array_env[i, :] = envelope(corr_deconv_array[i, :])

    half_x_axis = int(np.ceil(len(corr_deconv_array_env[0])/2))
    env_max = np.argmax(corr_deconv_array_env[:,half_x_axis:half_x_axis+2000], axis=1)  # Index of maximum value
        # of envelope
    env_max_sec = env_max / 1000
    env_max_deconv_data = np.array([time_events, env_max_sec])
    env_max_deconv_data = env_max_deconv_data.T
    output_filename = 'env_max_deconv_out.dat'
    np.savetxt(output_filename, env_max_deconv_data, delimiter='\t', header='Day\tTime_when_envelope_has_maximum_value')
    print(output_filename, ' was saved')

    data2 = (corr_deconv_array, corr_deconv_array_env, half_x_axis, env_max, env_max_sec)
    return data2

def plotting():
    mult_factor = 5  # Multiplication factor for traces amplitude on the plot
    for i in range(0, len(traces1_norm), 2):
        #plt.plot((corr_deconv_array[i,:] / max(corr_deconv_array[i,:])) * mult_factor + time_events[i])  # Plot of traces
        plt.plot((corr_deconv_array_env[i, :] / max(corr_deconv_array_env[i, :])) * mult_factor + time_events[i], '--')
    plt.scatter(env_max + half_x_axis, time_events)
    plt.xlim(0, len(corr_deconv_array[0]))
    plt.ylim(time_events[0]-1, time_events[-1]+1)
    plt.xlabel('Time [s]')
    plt.ylabel('Days')
    plt.title('Deconvolved traces for stations ' + station1 + ' (component ' + component1 + ')' + ' and ' + station2 +
              ' (component ' + component2 + ')' + '\nBandpass ' + str(bandpass_down) + ' - ' + str(bandpass_up) + ' Hz')
    x_ticks = np.arange(192, 16193, 500)  # Ticks in miliseconds
    my_x_ticks = np.arange(-16, 17)  # New ticks in seconds, and with zero in the middle
    plt.xticks(x_ticks, my_x_ticks)
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    importing()
    calculations(traces1, traces1_norm, traces2, traces2_norm, time_events)
    plotting()
#else:
#    calculations()