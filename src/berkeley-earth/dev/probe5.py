from subsets_utils import get
import netCDF4 as nc
S3="https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/"
for f in ["Global/Land_and_Ocean_complete.txt","Global/Complete_TAVG_complete.txt",
          "Global/Complete_TMAX_complete.txt","Global/Complete_TMIN_complete.txt"]:
    r=get(S3+f, timeout=(8,60), headers={"Range":"bytes=0-50"})
    print(f, r.status_code)
# in-memory netcdf open
r=get(S3+"Global/Gridded/Complete_TAVG_EqualArea.nc", timeout=(10,300))
ds=nc.Dataset("inmem", memory=r.content)
print("inmem open ok; temp shape", ds.variables['temperature'].shape, "clim", ds.variables['climatology'].shape)
