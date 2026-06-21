import numpy as np, pyarrow as pa
SCHEMA = pa.schema([
  ("variable", pa.string()),("date", pa.date32()),("year", pa.int16()),("month", pa.int8()),
  ("latitude", pa.float64()),("longitude", pa.float64()),("land_fraction", pa.float64()),
  ("temperature_anomaly", pa.float64()),
])
times=np.array([1750.04166667,1750.125,2024.625],dtype='float64')
yrs=np.floor(times).astype(int)
mos=np.clip(np.round((times-yrs)*12+0.5).astype(int),1,12)
print("yrs",yrs,"mos",mos)
date_m=np.array([f"{y:04d}-{m:02d}" for y,m in zip(yrs,mos)],dtype='datetime64[M]')
date_d=date_m.astype('datetime64[D]')
P=2
lat=np.array([10.0,20.0]); lon=np.array([-5.0,5.0]); land=np.array([0.3,1.0])
arr=np.array([[1.5,np.nan],[2.5,3.5],[np.nan,np.nan]])  # (3,2)
nT=3
temps=arr.ravel()
lat_r=np.tile(lat,nT); lon_r=np.tile(lon,nT); land_r=np.tile(land,nT)
yr_r=np.repeat(yrs,P); mo_r=np.repeat(mos,P); date_r=np.repeat(date_d,P)
m=~np.isnan(temps); n=int(m.sum())
b=pa.record_batch([
  pa.array(np.full(n,"TAVG"),type=pa.string()),
  pa.array(date_r[m],type=pa.date32()),
  pa.array(yr_r[m].astype('int16'),type=pa.int16()),
  pa.array(mo_r[m].astype('int8'),type=pa.int8()),
  pa.array(lat_r[m],type=pa.float64()),
  pa.array(lon_r[m],type=pa.float64()),
  pa.array(land_r[m],type=pa.float64()),
  pa.array(temps[m],type=pa.float64()),
],schema=SCHEMA)
print(b.to_pandas().to_string())
# date32 ts conversion
import datetime
print("ts date32 ok:", pa.array([datetime.date(1850,1,1)],type=pa.date32()))
