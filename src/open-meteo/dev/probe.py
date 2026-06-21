import json
from subsets_utils import get

def show(label, url, params):
    r = get(url, params=params, timeout=(10, 120))
    print("\n===", label, "->", r.status_code)
    try:
        d = r.json()
    except Exception:
        print("non-json:", r.text[:300]); return
    if isinstance(d, dict):
        print("top keys:", list(d.keys()))
        for g in ("daily", "hourly"):
            if g in d:
                gd = d[g]
                print(f"  {g} keys:", list(gd.keys()))
                t = gd.get("time", [])
                print(f"  {g} time[0,-1]:", t[:1], t[-1:], "n=", len(t))
                for k, v in gd.items():
                    if k != "time":
                        print(f"    {k}: sample {v[:2]} units={d.get(g+'_units',{}).get(k)}")
        if "error" in d:
            print("  ERROR:", d.get("reason"))

# 1. climate single model — are columns suffixed?
show("climate single model", "https://climate-api.open-meteo.com/v1/climate", {
    "latitude": 52.52, "longitude": 13.41,
    "start_date": "1950-01-01", "end_date": "1950-01-05",
    "models": "MRI_AGCM3_2_S",
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_mean,shortwave_radiation_sum,relative_humidity_2m_mean",
})

# 2. air quality reanalysis start_date support + domain
show("air-quality archive", "https://air-quality-api.open-meteo.com/v1/air-quality", {
    "latitude": 52.52, "longitude": 13.41,
    "start_date": "2013-01-01", "end_date": "2013-01-02",
    "domains": "cams_global",
    "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index",
})

# 3. archive full daily var set
show("archive daily", "https://archive-api.open-meteo.com/v1/archive", {
    "latitude": 52.52, "longitude": 13.41,
    "start_date": "1940-01-01", "end_date": "1940-01-03",
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration",
    "timezone": "GMT",
})

# 4. flood vars
show("flood daily", "https://flood-api.open-meteo.com/v1/flood", {
    "latitude": 52.52, "longitude": 13.41,
    "start_date": "1984-01-01", "end_date": "1984-01-03",
    "daily": "river_discharge",
})

# 5. flood with mean/max/min
show("flood daily ensemble vars", "https://flood-api.open-meteo.com/v1/flood", {
    "latitude": 52.52, "longitude": 13.41,
    "start_date": "1984-01-01", "end_date": "1984-01-03",
    "daily": "river_discharge,river_discharge_mean,river_discharge_max,river_discharge_min",
})
