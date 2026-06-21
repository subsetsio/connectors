from subsets_utils import get
def vals(label, params):
    r = get("https://air-quality-api.open-meteo.com/v1/air-quality", params=params, timeout=(10,120))
    d = r.json()
    if "error" in d: print(label, "ERROR", d.get("reason")); return
    gd = d.get("hourly", {})
    pm = [x for x in gd.get("pm10",[]) if x is not None]
    t = gd.get("time",[""])
    print(f"{label}: t={t[0]}..{t[-1]} pm10 nonnull={len(pm)}/{len(gd.get('pm10',[]))} sample={pm[:2]}")

# recent windows, default domain
vals("past_days=7 no domain", {"latitude":52.52,"longitude":13.41,"past_days":7,"forecast_days":1,"hourly":"pm10"})
for sd,ed in [("2025-01-01","2025-01-02"),("2024-06-01","2024-06-02"),("2023-06-01","2023-06-02"),("2024-06-01","2024-06-02")]:
    vals(f"range {sd} (auto)", {"latitude":52.52,"longitude":13.41,"start_date":sd,"end_date":ed,"hourly":"pm10"})
    vals(f"range {sd} (cams_europe)", {"latitude":52.52,"longitude":13.41,"start_date":sd,"end_date":ed,"domains":"cams_europe","hourly":"pm10"})
