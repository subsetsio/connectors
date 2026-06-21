import time
from subsets_utils import get
def timeit(label, url, params):
    t=time.time(); r=get(url,params=params,timeout=(10,180)); d=r.json()
    g="hourly" if "hourly" in d else "daily"
    n=len(d.get(g,{}).get("time",[]))
    print(f"{label}: {r.status_code} rows={n} bytes={len(r.content)} {time.time()-t:.1f}s")
timeit("archive full 1940-2025", "https://archive-api.open-meteo.com/v1/archive",
   {"latitude":51.51,"longitude":-0.13,"start_date":"1940-01-01","end_date":"2025-06-01",
    "daily":"temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration","timezone":"GMT"})
timeit("AQ full 2013-2025 hourly", "https://air-quality-api.open-meteo.com/v1/air-quality",
   {"latitude":51.51,"longitude":-0.13,"start_date":"2013-01-01","end_date":"2025-06-01",
    "hourly":"pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index"})
timeit("climate full 1950-2050", "https://climate-api.open-meteo.com/v1/climate",
   {"latitude":51.51,"longitude":-0.13,"start_date":"1950-01-01","end_date":"2050-12-31","models":"MRI_AGCM3_2_S",
    "daily":"temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_mean,shortwave_radiation_sum,relative_humidity_2m_mean"})
timeit("flood full 1984-2025", "https://flood-api.open-meteo.com/v1/flood",
   {"latitude":51.51,"longitude":-0.13,"start_date":"1984-01-01","end_date":"2025-06-01","daily":"river_discharge"})
