import sys, tempfile, os; sys.path.insert(0, "src")
import subsets_utils as su
import netCDF4, numpy as np
base="https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Gridded/"
for f in ["Complete_TMAX_EqualArea.nc"]:
    r=su.get(base+f, timeout=(10,600))
    tf=tempfile.NamedTemporaryFile(suffix=".nc", delete=False); tf.write(r.content); tf.close()
    ds=netCDF4.Dataset(tf.name)
    print(f, "dims:", {k:len(v) for k,v in ds.dimensions.items()})
    t=ds.variables['temperature']
    print(" temperature _FillValue:", getattr(t,'_FillValue','none'), "missing_value:", getattr(t,'missing_value','none'))
    sl=t[0,:]  # first time slice
    print(" type:", type(sl), "masked count:", np.ma.count_masked(sl) if np.ma.isMA(sl) else 'n/a', "of", sl.size)
    print(" sample temps:", np.asarray(sl).ravel()[:5])
    tm=t[-1,:]
    print(" last-slice nan count:", int(np.isnan(np.asarray(tm)).sum()))
    print(" time range:", float(ds.variables['time'][0]), float(ds.variables['time'][-1]))
    ds.close(); os.unlink(tf.name)
