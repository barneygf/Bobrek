'''Maciej Barnaś, maciej.michal.barnas@gmail.com
File contains functions for importing data for Bobrek coal mine (data from IS-EPOS platform).
Last edit: 2017-05-24'''

from obspy import read
import os
import scipy
import scipy.io
import numpy as np
import pandas as pd

def import_seeds(path_begin = 'e:\Maciek_Barnas\Bobrek\\01.2010_ML1.2_Z-600\\'):  # Path to folder with .seed files
    for root, dirs, files in os.walk(path_begin):
        a = files  # Get list of files (in this case - seeds) in folder

    print('SEED files: ', a)
    traces = read(path_begin + a[0])  # Read Traces from first file. In the loop below Traces from files are attached
    # to Stream, so it is necessary to read first file here.

    for i in range(1, len(a)):
        traces += read(path_begin + a[i])  # Read succesive files

    return traces

def select_seeds(input_traces, station, component, bandpass_down=None, bandpass_up=None, norm=None):
    traces_select = input_traces.select(station=station, component=component)  # Select Traces from one seismometer and one
        # component
    if bandpass_down != None and bandpass_up != None:
        traces_select.filter(type='bandpass', freqmin=bandpass_down, freqmax=bandpass_up)  # Bandpass filter (it overwrites data)
    if bandpass_down != None and bandpass_up == None:
        traces_select.filter(type='highpass', freq=bandpass_down)
    if bandpass_down == None and bandpass_up != None:
        traces_select.filter(type='lowpass', freq=bandpass_up)
    if norm == True:
        traces_select.normalize()

    return traces_select

def import_time_events(file='BOBREK_catalog_01.2010_ML1.2_Z-600.mat'):
    BOBREK_catalog = scipy.io.loadmat(file)
    catalog = BOBREK_catalog['Ctg']
    time_events1 = np.empty([len(catalog[0, 0][2])])
    for i in range(len(catalog[0, 0][2])):
        time_events1[i] = catalog[0, 1][2][i][0]

    time_events = np.empty([len(time_events1)])
    for i in range(len(time_events1)):
        time_events[i] = time_events1[i] - min(time_events1)  # Now first event has time equal to zero

    return time_events

def import_events(file, catalog='Ctg'):
    BOBREK_catalog = scipy.io.loadmat(file)
    catalog = BOBREK_catalog[catalog]  # Check this name - IS-EPOS changed "Catalog" to "Ctg" in April 2017,
    # so the name depends on when you download .mat file

    temp_ID = []
    for i in range(len(catalog[0, 0][2])):
        temp_ID.append(catalog[0, 0][2][i][0][0])

    Bobrek = {}
    Bobrek[str(catalog[0, 0][0][0])] = temp_ID

    for i in range(1, len(catalog[0])):
        temp = []
        for j in range(len(catalog[0, 0][2])):
            temp.append(catalog[0, i][2][j][0])
        Bobrek[str(catalog[0, i][0][0])] = temp

    return pd.DataFrame(Bobrek)  # Dataframe with events

def import_stations(stations_file='Stations.xlsx'):
    stations_Excel = pd.ExcelFile(stations_file)
    stations = stations_Excel.parse('Arkusz1')  # Dataframe with stations

    return stations