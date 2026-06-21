from subsets_utils import get
import tempfile, os
import netCDF4 as nc
import numpy as np

# Download smallest full gridded file to inspect structure
S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Gridded/"
fn = "Complete_TAVG_EqualArea.nc"
r = get(S3+fn, timeout=(10,300))
print("downloaded", len(r.content), "bytes")
tf = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
tf.write(r.content); tf.close()
ds = nc.Dataset(tf.name)
print("FORMAT:", ds.data_model)
print("DIMS:", {d: len(ds.dimensions[d]) for d in ds.dimensions})
print("VARS:")
for v in ds.variables:
    var = ds.variables[v]
    print("  ", v, var.dimensions, var.shape, var.dtype, "| units:", getattr(var,'units','?'))
# sample a few coordinate values
for c in ("time","longitude","latitude","month_number","map_pts"):
    if c in ds.variables:
        arr = ds.variables[c][:]
        print(c, "->", np.asarray(arr).ravel()[:5], "... n=", np.asarray(arr).size)
os.unlink(tf.name)
