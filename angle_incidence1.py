from def_import_Bobrek import import_events, import_stations
from mpl_toolkits.basemap import pyproj
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import ceil
from cm2inch import cm2inch
from matplotlib import gridspec

events = import_events(file='BOBREK_catalog_01.2010_ML1.2_Z-600.mat')
stations = import_stations()
stations.index = stations["Code"]

PL2000VI = pyproj.Proj("+init=EPSG:2177")  # ETRS89 / Poland CS2000 zone 6

# Convert geographical coordinates of the stations to Poland CS2000 zone 6 coordinates
for lab, row in stations.iterrows():
    stations.loc[lab, 'Y_2000'], stations.loc[lab, 'X_2000'] = PL2000VI(row['Longitude'], row['Latitude'])

# Convert geographical coordinates of the events to Poland CS2000 zone 6 coordinates
for lab, row in events.iterrows():
    events.loc[lab, 'Y_2000'], events.loc[lab, 'X_2000'] = PL2000VI(row['Long'], row['Lat'])

# Adding column with event number
for lab, row in events.iterrows():
    events.loc[lab, 'nr'] = events.loc[lab, 'ID'][17:]

events[['nr']] = events[['nr']].apply(pd.to_numeric)
events.index = events['nr']

k1 = np.empty((len(events), 3))  # There are 3 coordinates in 3-dimensional space
#k2 = np.empty((len(events), 3))

station1 = 'S013'  # Surface station
station2 = 'S015'  # Underground station
x_station1 = stations.loc[station1, 'X_2000']
y_station1 = stations.loc[station1, 'Y_2000']
z_station1 = stations.loc[station1, 'Elevation']
x_station2 = stations.loc[station2, 'X_2000']
y_station2 = stations.loc[station2, 'Y_2000']
z_station2 = stations.loc[station2, 'Elevation']

for i in range(len(events)):
    k1[i, 0] = x_station1 - events.iloc[i, 12]  # X_2000 is in 12. column in events DataFrame
    k1[i, 1] = y_station1 - events.iloc[i, 11]  # Y_2000 is in 11. column in events DataFrame
    k1[i, 2] = z_station1 - events.iloc[i, 10]  # Z is in 10. column in events DataFrame
    #k2[i, 0] = x_station2 - events.iloc[i, 12]  # X_2000 is in 12. column in events DataFrame
    #k2[i, 1] = y_station2 - events.iloc[i, 11]  # Y_2000 is in 11. column in events DataFrame
    #k2[i, 2] = z_station2 - events.iloc[i, 10]  # Z is in 10. column in events DataFrame
# Now every row in k1 and k2 arrays corresponds with one seismic event. DataFrame k1 harmonizes with station1 and k2
# with station2. First column of arrays is difference in x coordinate between station and event, second in y coordinate
# and third in z coordinate.
k2 = np.array([x_station1 - x_station2, y_station1 - y_station2, z_station1 - z_station2])

#print('k1: ', k1)
#print('k2: ', k2)
denominator = np.empty(len(k1))
len_k1 = np.empty(len(k1))
len_k2 = np.sqrt(k2[0] ** 2 + k2[1] ** 2 + k2[2] ** 2)
#len_k2 = np.empty(len(k1))
angle = np.empty(len(k1))
for i in range(len(k1)):
    #denominator[i] = np.abs(k1[i, 0] * k2[i, 0] + k1[i, 1] * k2[i, 1] + k1[i, 2] + k2[i, 2])
    denominator[i] = np.abs(k1[i, 0] * k2[0] + k1[i, 1] * k2[1] + k1[i, 2] * k2[2])
    len_k1[i] = np.sqrt(k1[i, 0] ** 2 + k1[i, 1] ** 2 + k1[i, 2] ** 2)
    #len_k2[i] = np.sqrt(k2[i, 0] ** 2 + k2[i, 1] ** 2 + k2[i, 2] ** 2)
    angle[i] = np.arccos(denominator[i]/(len_k1[i] * len_k2))
    #angle[i] = np.arccos(denominator[i] / (len_k1[i] * len_k2[i]))

angle_deg = np.degrees(angle)
x = np.linspace(1, 201, num=200)

event_nr = 0
line1 = np.array([[x_station1, y_station1, z_station1], [events.iloc[event_nr, 12], events.iloc[event_nr, 11],
                                                         events.iloc[event_nr, 10]]])  # Line between event location
# and surface station
line2 = np.array([[x_station1, y_station1, z_station1], [x_station2, y_station2, z_station2]])  # Line between surface
# and underground station

cubic = np.empty((len(events) + 2, 3))
cubic[:-2, 0] = events.loc[:, 'X_2000']
cubic[:-2, 1] = events.loc[:, 'Y_2000']
cubic[:-2, 2] = events.loc[:, 'Z']
cubic[-1, 0] = x_station1
cubic[-1, 1] = y_station1
cubic[-1, 2] = z_station1
cubic[-2, 0] = x_station2
cubic[-2, 1] = y_station2
cubic[-2, 2] = z_station2

cubic_range = np.array([cubic[:, 0].max() - cubic[:, 0].min(), cubic[:, 1].max() - cubic[:, 1].min(),
                       cubic[:, 2].max() - cubic[:, 2].min()]).max()
X_cubic = 0.5 * cubic_range * np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5 * (cubic[:, 0].max() +
                                                                                   cubic[:, 0].min())
Y_cubic = 0.5 * cubic_range * np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5 * (cubic[:, 1].max() +
                                                                                   cubic[:, 1].min())
Z_cubic = 0.5 * cubic_range * np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5 * (cubic[:, 2].max() +
                                                                                   cubic[:, 2].min())

plt.figure(1)
plt.scatter(x, angle_deg)

fig = plt.figure(2, figsize=cm2inch(55, 30))
#plt.tight_layout()
gs = gridspec.GridSpec(2, 3)
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(gs[:, :2], projection='3d')
plt.axis('equal')
ax.scatter(events['X_2000'], events['Y_2000'], events['Z'], s=30, c=events['Time'], cmap='rainbow')
#ax.scatter(events.iloc[:, 12], events.iloc[:, 11], events.iloc[:, 10], s=30, c=events['Time'], cmap='rainbow')
ax.scatter(x_station1, y_station1, z_station1, marker='^', s=50, color='r')
ax.scatter(x_station2, y_station2, z_station2, marker='^', s=50, color='r')
ax.plot(line1[:, 0], line1[:, 1], line1[:, 2])
ax.plot(line2[:, 0], line2[:, 1], line2[:, 2])
for xc, yc, zc in zip(X_cubic, Y_cubic, Z_cubic):
   ax.plot([xc], [yc], [zc], 'w')

ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
plt.xticks(np.arange(ceil(min(cubic[:, 0]) / 200) * 200 - 200, ceil(max(cubic[:, 0]) / 200) * 200 + 200, 200))
plt.yticks(np.arange(ceil(min(cubic[:, 1]) / 200) * 200 - 200, ceil(max(cubic[:, 1]) / 200) * 200 + 200, 200))
#plt.zticks(np.arange(ceil(min(cubic[:, 2]) / 200) * 200, ceil(max(cubic[:, 2]) / 200) * 200, 200))

print('station1: ', x_station1, y_station1, z_station1)
print('station2: ', x_station2, y_station2, z_station2)
print('source: ', events.iloc[event_nr, 12], events.iloc[event_nr, 11], events.iloc[event_nr, 10])

print('vector 1:', x_station2-x_station1, y_station2-y_station1, z_station2-z_station1)
print('vector 2:', events.iloc[event_nr, 12]-x_station1, events.iloc[event_nr, 11]-y_station1,
      events.iloc[event_nr, 10]-z_station1)

print('k1: ', k1[0, :])
print('k2: ', k2)

print('denominator: ', denominator)

ax2 = fig.add_subplot(gs[0, 2])
ax2.hist(angle_deg, 10)
ax2.set_xlabel('Angle [$^\circ$C]')
ax2.set_ylabel('Number of events with given angle')
ax2.set_title('Histogram')

ax3 = fig.add_subplot(gs[1, 2])
ax3.hist(angle_deg, 10, cumulative=True, color='g')
ax3.set_xlabel('Angle [$^\circ$C]')
ax3.set_ylabel('Number of cumulative events with given angle')
ax3.set_title('Cumulative histogram')

plt.figtext(0.001, 0.03, 'Figure 4. On the left - chosen seismic events (ML > 1.2, z < 800 m b.s.l.),  stations (S013, '
                       'S015) - red triangles, and angle of incidence between two stations and some event (example);\n'
                       'Right upper - histogram of angles of incidence (angle between green and blue lines on the 3D '
                       'plot) for all chosen events\nRight down - same as upper, but this is cumulative histogram',
            horizontalalignment='left', fontsize=11, style='italic', backgroundcolor='w')

plt.tight_layout()
plt.show()
