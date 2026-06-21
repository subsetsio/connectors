from subsets_utils import get
import importlib
for mod in ("xarray","netCDF4","h5netcdf","scipy"):
    try:
        importlib.import_module(mod); print("HAVE", mod)
    except Exception as e:
        print("MISSING", mod)

# HEAD the gridded files to learn sizes
S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Gridded/"
for f in ["Complete_TAVG_LatLong1.nc","Complete_TAVG_EqualArea.nc","Land_and_Ocean_LatLong1.nc","Land_and_Ocean_EqualArea.nc"]:
    try:
        r = get(S3+f, timeout=(10,60), headers={"Range":"bytes=0-0"})
        cr = r.headers.get("content-range")
        print(f, r.status_code, "size=", cr)
    except Exception as e:
        print("ERR", f, type(e).__name__, str(e)[:100])
