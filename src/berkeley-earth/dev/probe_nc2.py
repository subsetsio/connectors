from subsets_utils import get
import tempfile, os
import netCDF4 as nc
import numpy as np

S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Gridded/"
for fn in ["Land_and_Ocean_EqualArea.nc"]:
    r = get(S3+fn, timeout=(10,300))
    print("===", fn, len(r.content), "bytes")
    tf = tempfile.NamedTemporaryFile(suffix=".nc", delete=False); tf.write(r.content); tf.close()
    ds = nc.Dataset(tf.name)
    print("DIMS:", {d: len(ds.dimensions[d]) for d in ds.dimensions})
    for v in ds.variables:
        var = ds.variables[v]
        print("  ", v, var.dimensions, var.shape, var.dtype, "units:", getattr(var,'units','?'))
    temp = ds.variables['temperature']
    # NaN fraction on a few time slices (first, mid, last)
    T = temp.shape[0]
    for ti in (0, T//2, T-1):
        sl = np.asarray(temp[ti,:])
        frac = np.isnan(sl).mean()
        print(f"  t={ti} time={float(ds.variables['time'][ti]):.3f} nan_frac={frac:.3f} sample={sl[~np.isnan(sl)][:3]}")
    print("  time range:", float(ds.variables['time'][0]), "->", float(ds.variables['time'][-1]))
    os.unlink(tf.name)
