"""Maciej Barnaś, maciej.michal.barnas@gmail.com
Program plots stations and events from 2010 year, with local magnitude greater than 1.2, below the 600 m b.s. l in
Bobrek coal mine (data from IS-EPOS platform).
Last edit: 2017-10-02"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import pyproj
from datetime import datetime
from def_import_Bobrek import import_events, import_stations
from numpy import arange
import plotly.plotly as py

print(__doc__)

Bobr = import_events(file='BOBREK_catalog_01.2010_ML1.2_Z-600.mat')  # Importing events from Matlab file
stations = import_stations()
PL2000VI = pyproj.Proj("+init=EPSG:2177") # ETRS89 / Poland CS2000 zone 6

# Convert geographical coordinates of the stations to Poland CS2000 zone 6 coordinates
for lab, row in stations.iterrows():
    stations.loc[lab, 'Y_2000'], stations.loc[lab, 'X_2000'] = PL2000VI(row['Longitude'], row['Latitude'])

# Convert geographical coordinates of the events to Poland CS2000 zone 6 coordinates
for lab, row in Bobr.iterrows():
    Bobr.loc[lab, 'Y_2000'], Bobr.loc[lab, 'X_2000'] = PL2000VI(row['Long'], row['Lat'])

# Adding column with event number
for lab, row in Bobr.iterrows():
    Bobr.loc[lab, 'nr'] = Bobr.loc[lab, 'ID'][17:]

Bobr[['nr']] = Bobr[['nr']].apply(pd.to_numeric)
events_2010 = Bobr['nr'] >= 932  # I checked on the IS-EPOS platform, that this event is first
    # after 2010 Jan 19 06:09:48.0 (date of installing some sensors), it would be difficult, to
    # check it in Python, because of 'Time' column - it doesn't contain dates, but big floats,
    # so converting it to dates takes a lot of time
Bobr1 = Bobr[events_2010]  # Events from 2010 Jan 19 06:09:48.0 to the end of the data

events_2010_below_800 = Bobr1['Z'] < -800
Bobr2 = Bobr1[events_2010_below_800]
events_2010_below_800_ML12 = Bobr2['ML'] >= 1.2
Bobr3 = Bobr2[events_2010_below_800_ML12]

fig = plt.figure()
ax1 = fig.add_subplot(121, projection='3d')
plt.tight_layout()
ax1.scatter(Bobr3['Y_2000'], Bobr3['X_2000'], Bobr3['Z'], s=30*Bobr3['ML'], c=Bobr3['ML'], cmap='rainbow')
ax1.scatter(stations['Y_2000'], stations['X_2000'], stations['Elevation'], marker='^', s=40, color='r')

for lab, row in stations.iterrows():
    ax1.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Elevation']+3,
            stations.loc[lab, 'Code'])

# ax1.set_xlabel('Latitide [\u00b0]')
# ax1.set_ylabel('Longitude [\u00b0]')
ax1.set_xlabel('Y [m]')
ax1.set_ylabel('X [m]')
ax1.set_zlabel('Z [m]', labelpad=20)
ax1.tick_params(axis='z', pad=12)
max_lat = 50.3716
min_lat = 50.3432
max_long = 18.8982
min_long = 18.8329
min_X_2000 = 5.57871e+06
max_X_2000 = 5.58212e+06
min_Y_2000 = 6.55971e+06
max_Y_2000 = 6.56377e+06
x_ticks = arange(5.579e6, 5.579e6+3500, 500)
y_ticks = arange(6.56e6, 6.56e6+4000, 500)
ax1.set_xlim([min_Y_2000, max_Y_2000])
ax1.set_ylim([min_X_2000, max_X_2000])
ax1.set_xticks(y_ticks)
ax1.set_yticks(x_ticks)

ax2 = fig.add_subplot(122)
#D = ax2.scatter(Bobr2['Y_2000'], Bobr2['X_2000'], c=Bobr2['ML'], cmap='rainbow', s=30)
#ax2.scatter(stations['Y_2000'], stations['X_2000'], marker='^', s=40, color='r')
#D = ax2.scatter(Bobr3['Long'], Bobr3['Lat'], c=Bobr3['ML'], cmap='rainbow', s=30)
D = ax2.scatter(Bobr3['Y_2000'], Bobr3['X_2000'], c=Bobr3['ML'], cmap='rainbow', s=30)
ax2.scatter(stations['Longitude'], stations['Latitude'], marker='^', s=40, color='r')
ax2.scatter(stations['Y_2000'], stations['X_2000'], marker='^', s=40, color='r')
#plt.plot([18.8670, 18.8717], [50.3547, 50.3546], c='y', linewidth=5)
#plt.plot([18.8670, 18.8717], [50.3515, 50.3515], c='y', linewidth=5)

for lab, row in stations.iterrows():
   ax2.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Code'])

# for lab, row in stations.iterrows():
#     ax2.text(stations.loc[lab, 'Longitude'], stations.loc[lab, 'Latitude'], stations.loc[lab, 'Code'])

ax2.set_xlabel('Y [m]')
ax2.set_ylabel('X [m]')
# ax2.set_xlabel('Longitude [\u00b0]')
# ax2.set_ylabel('Latitude [\u00b0]')
cbar = fig.colorbar(D, orientation='horizontal')
cbar.set_label('Local magnitude')
# ax2.set_xlim([min_long, max_long])
# ax2.set_ylim([min_lat, max_lat])
ax2.set_xlim([min_Y_2000, max_Y_2000])
ax2.set_ylim([min_X_2000, max_X_2000])
ax2.set_xticks(y_ticks)
ax2.set_yticks(x_ticks)
ax2.grid()

plt.figtext(0.5, 0.03, 'Figure 2. Seismic events with magnitude higher than 1.2 and location below 800 m b.s.l. '
                        '(points) - color responds magnitude; stations - red triangles with labels; on the left - 3D '
                        'plot, on the right - 2D map',
            horizontalalignment='center', fontsize=11, style='italic', backgroundcolor='w')

plt.show()