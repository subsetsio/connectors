import sys; sys.path.insert(0, "src")
import subsets_utils as su
import netCDF4, numpy as np

u = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Gridded/Complete_TAVG_EqualArea.nc"
r = su.get(u, timeout=(10, 600))
print("downloaded bytes:", len(r.content))
ds = netCDF4.Dataset("inmem", mode="r", memory=r.content)
print("dims:", {k: len(v) for k, v in ds.dimensions.items()})
print("--- variables ---")
for vn, v in ds.variables.items():
    print(f"  {vn} dims={v.dimensions} shape={v.shape} dtype={v.dtype} units={getattr(v,'units','?')}")
for cn in ["time", "longitude", "latitude", "land_mask"]:
    if cn in ds.variables:
        arr = np.asarray(ds.variables[cn][:]).ravel()
        print(f"  {cn}: first={arr[:4]} last={arr[-3:]} n={arr.size}")
# temperature shape + a slice
t = ds.variables["temperature"]
print("temperature shape:", t.shape)
sl = np.asarray(t[0, :])
print("first time slice nan count:", int(np.isnan(sl).sum()), "of", sl.size)
sl2 = np.asarray(t[-1, :])
print("last time slice nan count:", int(np.isnan(sl2).sum()), "of", sl2.size)
print("sample non-nan temps:", sl[~np.isnan(sl)][:5])
# estimate total non-null rows
print("time len:", t.shape[0], "cells:", t.shape[1], "max rows:", t.shape[0]*t.shape[1])
ds.close()
