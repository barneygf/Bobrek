import pandas as pd
from obspy.core import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import def_import_Bobrek
from scipy.stats import linregress
from scipy.interpolate import splev, splrep

Bobr = def_import_Bobrek.import_events(file='BOBREK_catalog_01.2010_ML1.2_Z-600.mat')
sd = 86400  # Amount of seconds in day
time_dif1 = UTCDateTime(Bobr['Time'].iat[0] * sd) - UTCDateTime('2010-01-22T11:08:47.1')
time_dif2 = UTCDateTime(Bobr['Time'].iat[-1] * sd) - UTCDateTime('2010-06-23T11:49:12.5')

time_difs = [time_dif1, time_dif2]
for lab, row in Bobr.iterrows():
    Bobr.loc[lab, 'UTC_Time'] = UTCDateTime(row['Time'] * sd - np.mean(time_difs))

start_meas = UTCDateTime(2010, 1, 22)
end_meas = UTCDateTime(2010, 6, 23)
#print((end_meas - start_meas) / sd)

time = [start_meas + i * sd for i in range(int((end_meas - start_meas) / sd) + 1)]  # List with days from
    # measurements start to end, one day interval
t_distance = 10
time_distance = [start_meas + i * sd for i in range(0, int((end_meas - start_meas) / sd) + 1, t_distance)]

days_energy = np.zeros(int((end_meas - start_meas) / sd) + 1)

for i in range(len(Bobr)):
    for j in range(len(time)):
        if time[j] <= Bobr['UTC_Time'].iat[i] < time[j] + sd:
            days_energy[j] += Bobr['E'].iat[i]

#print(days_energy)
time_ticks = [i for i in range(0, int((end_meas - start_meas) / sd) + 1, t_distance)]
#print(time_distance)

input_filename = 'env_max_out.dat'
time_event, env_corr_max = np.loadtxt(input_filename, delimiter='\t', skiprows=1, unpack=True)
env_deconv_max = np.loadtxt(input_filename, delimiter='\t', skiprows=1, usecols=(1,), unpack=True)
#print('time event ', time_event)
#print('env corr max ', env_corr_max)
#print('env deconv max ', env_deconv_max)

time_daily = [i-0.5 for i in range(int((end_meas - start_meas) / sd) + 1)]
#print(time_daily)
#print(len(time_daily))
#print(time_daily)


fig, ax1 = plt.subplots()

ax1.bar(time_daily, days_energy, color='b', width=1)
ax1.set_xlabel('Days')
ax1.set_ylabel('Energy', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.scatter(time_event, env_corr_max, c='r')
ax2.set_ylabel('Time of maximum value of signal envelope [s]', color='r')
ax2.tick_params('y', colors='r', )
ax2.set_ylim(0, 2)

ax3 = ax1.twinx()
ax3.scatter(time_event, env_deconv_max, c='g')
ax3.set_ylim(0, 2)
slope_d, intercept_d, r_value_d, p_value_d, std_err_d = linregress(time_event, env_deconv_max)  # Parameters of linear
    #regression for deconvolution points
ax3.plot(time_event, slope_d*time_event + intercept_d, 'g--')  # Plot linear regression line
ax3.text(x=135, y=0.4, s='linear regression\nR = ' + str('%.4f' % r_value_d), color='g')  # Add text with R coefficient
spl_d = splrep(time_event, env_deconv_max)
time_event_splrep = np.linspace(np.min(time_event), np.max(time_event), 25)
env_deconv_max_splrep = splev(time_event_splrep, spl_d)
ax3.plot(time_event_splrep, env_deconv_max_splrep, 'g')
print(time_event)

plt.title('Energy of seismic events per day with times of maximum value of signal envelope')
plt.xlim(-0.5,len(time_daily)+0.5)
plt.tight_layout()
plt.show()