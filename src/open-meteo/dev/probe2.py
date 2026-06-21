from subsets_utils import get

def vals(label, url, params):
    r = get(url, params=params, timeout=(10, 120))
    d = r.json()
    g = "hourly" if "hourly" in d else "daily"
    gd = d.get(g, {})
    out = {}
    for k, v in gd.items():
        if k == "time":
            continue
        nn = [x for x in v if x is not None]
        out[k] = f"n={len(v)} nonnull={len(nn)} sample={nn[:2]}"
    print(f"\n=== {label} [{r.status_code}] {g} t={gd.get('time',[''])[0]}..{gd.get('time',[''])[-1]}")
    for k, s in out.items():
        print(f"   {k}: {s}")

# air-quality at various starts
vals("AQ 2016-01", "https://air-quality-api.open-meteo.com/v1/air-quality", {
    "latitude": 52.52, "longitude": 13.41, "start_date": "2016-01-01", "end_date": "2016-01-02",
    "domains": "cams_global", "hourly": "pm10,pm2_5,ozone,nitrogen_dioxide,carbon_monoxide,sulphur_dioxide,dust,aerosol_optical_depth,uv_index"})
vals("AQ 2022-06", "https://air-quality-api.open-meteo.com/v1/air-quality", {
    "latitude": 52.52, "longitude": 13.41, "start_date": "2022-06-01", "end_date": "2022-06-02",
    "domains": "cams_global", "hourly": "pm10,pm2_5,ozone,nitrogen_dioxide,carbon_monoxide,sulphur_dioxide,dust,aerosol_optical_depth,uv_index"})

# flood at major river cities, recent
for nm, la, lo in [("Cairo-Nile", 30.04, 31.24), ("London-Thames", 51.51, -0.13), ("Berlin", 52.52, 13.41)]:
    vals(f"flood {nm} 2020", "https://flood-api.open-meteo.com/v1/flood", {
        "latitude": la, "longitude": lo, "start_date": "2020-01-01", "end_date": "2020-01-03",
        "daily": "river_discharge"})
