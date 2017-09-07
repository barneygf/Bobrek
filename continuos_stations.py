'''Maciej Barnaś, maciej.michal.barnas@gmail.com
Program prints pandas dataframe with stations. Main purpose is to check which stations were working all the time.
Last edit: 2017-05-24'''

from mpl_toolkits.basemap import pyproj
from def_import_Bobrek import import_stations

stations = import_stations()

PL2000VI = pyproj.Proj("+init=EPSG:2177")  # ETRS89 / Poland CS2000 zone 6

for lab, row in stations.iterrows():
    stations.loc[lab, 'Y_2000'], stations.loc[lab, 'X_2000'] = PL2000VI(row['Longitude'], row['Latitude'])

print(stations)