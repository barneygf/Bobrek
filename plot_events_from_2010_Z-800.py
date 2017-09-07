'''Maciej Barnaś, maciej.michal.barnas@gmail.com
Program plots stations and events from 2010 year, below the 800 m b.s.l. in Bobrek coal mine (data from IS-EPOS
platform).
Last edit: 2017-05-24'''

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import pyproj
from datetime import datetime
from def_import_Bobrek import import_events

Bobr = import_events(file='Bobrek_2010_-800_catalog.mat')  # Importing events from Matlab file

stations_file = 'Stations.xlsx'
stations_Excel = pd.ExcelFile(stations_file)
stations = stations_Excel.parse('Arkusz1')  # Dataframe with stations

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

events_2010_below_600 = Bobr1['Z'] < -600
Bobr2 = Bobr1[events_2010_below_600]
events_2010_below_600_ML12 = Bobr2['ML'] >= 1.2
Bobr3 = Bobr2[events_2010_below_600_ML12]

print(Bobr3)
print(stations)

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
plt.tight_layout()
ax.scatter(Bobr3['Y_2000'], Bobr3['X_2000'], Bobr3['Z'], s=60*Bobr3['ML'], c=Bobr3['ML'], cmap='rainbow')
ax.scatter(stations['Y_2000'], stations['X_2000'], stations['Elevation'], marker='^', s=40, color='r')

for lab, row in stations.iterrows():
    ax.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Elevation']+3,
            stations.loc[lab, 'Code'])

#ax.set_xlabel('Latitide [\u00b0]')
#ax.set_ylabel('Longitude [\u00b0]')
ax.set_xlabel('Y [m]')
ax.set_ylabel('X [m]')
ax.set_zlabel('Z [m]', labelpad=12)
max_lat = 50.3716
min_lat = 50.3432
max_long = 18.8982
min_long = 18.8329
min_X_2000 = 5.57871e+06
max_X_2000 = 5.58212e+06
min_Y_2000 = 6.55971e+06
max_Y_2000 = 6.56377e+06
ax.set_xlim([min_Y_2000, max_Y_2000])
ax.set_ylim([min_X_2000, max_X_2000])

ax = fig.add_subplot(122)
#D = ax.scatter(Bobr2['Y_2000'], Bobr2['X_2000'], c=Bobr2['ML'], cmap='rainbow', s=30)
#ax.scatter(stations['Y_2000'], stations['X_2000'], marker='^', s=40, color='r')
D = ax.scatter(Bobr3['Long'], Bobr3['Lat'], c=Bobr3['ML'], cmap='rainbow', s=30)
ax.scatter(stations['Longitude'], stations['Latitude'], marker='^', s=40, color='r')
plt.plot([18.8670, 18.8717], [50.3547, 50.3546], c='y', linewidth=5)
plt.plot([18.8670, 18.8717], [50.3515, 50.3515], c='y', linewidth=5)

#for lab, row in stations.iterrows():
#    ax.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Code'])

for lab, row in stations.iterrows():
    ax.text(stations.loc[lab, 'Longitude'], stations.loc[lab, 'Latitude'], stations.loc[lab, 'Code'])

#ax.set_xlabel('Y [m]')
#ax.set_ylabel('X [m]')
ax.set_xlabel('Longitude [\u00b0]')
ax.set_ylabel('Latitude [\u00b0]')
cbar = fig.colorbar(D, orientation='horizontal')
cbar.set_label('Local magnitude')
ax.set_xlim([min_long, max_long])
ax.set_ylim([min_lat, max_lat])

plt.show()