import def_import_Bobrek
import numpy as np
from obspy.core.trace import Stats

traces = def_import_Bobrek.import_seeds()
traces1 = def_import_Bobrek.select_seeds(traces, 'S013', 'Z')
traces2 = def_import_Bobrek.select_seeds(traces, 'S015', 'Z')

n = 49
traces1e = traces1[n]
traces2e = traces2[n]

fs = traces1e.stats.sampling_rate
npts = traces1e.stats.npts
times = np.linspace((1 / fs), (1 / fs) * npts, npts)

np.savetxt('Bobrek_export.dat', np.c_[times, traces1e, traces2e], delimiter='\t',
           header='time\tS013\tS015\tfs=500.0 Hz', comments='')