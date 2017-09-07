'''Maciej Barnaś, maciej.michal.barnas@gmail.com
On first figure program plots stations and all events in Bobrek coal mine (data from IS-EPOS platform). On second
figure one chosen events is plotted.
Last edit: 2017-05-24'''

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import pyproj
from def_import_Bobrek import import_events

Bobr = import_events(file='Bobrek_catalog.mat', catalog='Catalog')

stations_file = 'Stations.xlsx'
stations_Excel = pd.ExcelFile(stations_file)
stations = stations_Excel.parse('Arkusz1')

PL2000VI = pyproj.Proj("+init=EPSG:2177") # ETRS89 / Poland CS2000 zone 6

for lab, row in stations.iterrows():
    stations.loc[lab, 'Y_2000'], stations.loc[lab, 'X_2000'] = PL2000VI(row['Longitude'], row['Latitude'])

for lab, row in Bobr.iterrows():
    Bobr.loc[lab, 'Y_2000'], Bobr.loc[lab, 'X_2000'] = PL2000VI(row['Long'], row['Lat'])

for lab, row in Bobr.iterrows():
    Bobr.loc[lab, 'nr'] = Bobr.loc[lab, 'ID'][17:]

print(stations)
print(Bobr)

dif = 50

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
plt.tight_layout()
ax.scatter(Bobr['Y_2000'], Bobr['X_2000'], Bobr['Z'], s=60*Bobr['ML'])
ax.scatter(stations['Y_2000'], stations['X_2000'], stations['Elevation'], marker='^', s=40, color='r')

for lab, row in stations.iterrows():
    ax.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Elevation']+3,
            stations.loc[lab, 'Code'])

for lab, row in Bobr.iterrows():
    if Bobr.loc[lab, 'Y_2000'] - stations.loc[21, 'Y_2000'] < dif:
        if Bobr.loc[lab, 'X_2000'] - stations.loc[21, 'X_2000'] < dif:
            if Bobr.loc[lab, 'Z'] - stations.loc[21, 'Elevation'] < dif:
                ax.text(Bobr.loc[lab, 'Y_2000'], Bobr.loc[lab, 'X_2000']+3, Bobr.loc[lab, 'Z'],
                    Bobr.loc[lab, 'nr'], fontsize=6)

ax.set_xlabel('Latitide [\u00b0]')
ax.set_ylabel('Longitude [\u00b0]')
ax.set_zlabel('Z [km]', labelpad=12)
#max_lat = 50.3716
#min_lat = 50.3432
#max_long = 18.8982
#min_long = 18.8329
min_X_2000 = 5.57871e+06
max_X_2000 = 5.58212e+06
min_Y_2000 = 6.55971e+06
max_Y_2000 = 6.56377e+06
ax.set_xlim([min_Y_2000, max_Y_2000])
ax.set_ylim([min_X_2000, max_X_2000])

ax = fig.add_subplot(122)
D = ax.scatter(Bobr['Y_2000'], Bobr['X_2000'], c=Bobr['ML'], cmap='rainbow', s=30)
ax.scatter(stations['Y_2000'], stations['X_2000'], marker='^', s=40, color='r')

for lab, row in stations.iterrows():
    ax.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Code'])

for lab, row in Bobr.iterrows():
    if Bobr.loc[lab, 'Y_2000'] - stations.loc[21, 'Y_2000'] < dif:
        if Bobr.loc[lab, 'X_2000'] - stations.loc[21, 'X_2000'] < dif:
            ax.text(Bobr.loc[lab, 'Y_2000'], Bobr.loc[lab, 'X_2000']+3, Bobr.loc[lab, 'nr'], fontsize=6)

ax.set_xlabel('Y [m]')
ax.set_ylabel('X [m]')
cbar = fig.colorbar(D, orientation='horizontal')
cbar.set_label('Local magnitude')
ax.set_xlim([min_Y_2000, max_Y_2000])
ax.set_ylim([min_X_2000, max_X_2000])

#plt.show()
print('Kolumna z czasem: ', Bobr.iloc[:, 7])
print('Różnica czasu między pierwszym wydarzeniem, a ostatnim: ', Bobr.iloc[0, 7] - Bobr.iloc[-1, 7])

moje = Bobr['ID'] == 'BOBREK_CIBIS_KWB_1034'
print(Bobr[moje])

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(121, projection='3d')
plt.tight_layout()
ax2.scatter(Bobr[moje]['Y_2000'], Bobr[moje]['X_2000'], Bobr[moje]['Z'], s=60)
ax2.scatter(stations['Y_2000'], stations['X_2000'], stations['Elevation'], marker='^', s=40, color='r')
for lab, row in stations.iterrows():
    ax2.text(stations.loc[lab, 'Y_2000']+3, stations.loc[lab, 'X_2000']+3, stations.loc[lab, 'Elevation']+3,
             stations.loc[lab, 'Code'])

ax2.set_xlabel('Latitide [\u00b0]')
ax2.set_ylabel('Longitude [\u00b0]')
ax2.set_zlabel('Z [km]', labelpad=12)
ax2.set_xlim([min_Y_2000, max_Y_2000])
ax2.set_ylim([min_X_2000, max_X_2000])

ax2 = fig2.add_subplot(122)
D2 = ax.scatter(Bobr[moje]['Y_2000'], Bobr[moje]['X_2000'], s=30)
ax2.scatter(stations['Y_2000'], stations['X_2000'], marker='^', s=40, color='r')
ax.set_xlabel('Y [m]')
ax.set_ylabel('X [m]')
cbar = fig.colorbar(D, orientation='horizontal')
cbar.set_label('Local magnitude')
ax.set_xlim([min_Y_2000, max_Y_2000])
ax.set_ylim([min_X_2000, max_X_2000])

plt.show()