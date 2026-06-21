from subsets_utils import get
def chk(sd):
    r = get("https://air-quality-api.open-meteo.com/v1/air-quality",
            params={"latitude":52.52,"longitude":13.41,"start_date":sd,"end_date":sd,"hourly":"pm10"}, timeout=(10,120))
    d=r.json()
    if "error" in d: print(sd,"ERROR",d.get("reason")); return
    pm=[x for x in d.get("hourly",{}).get("pm10",[]) if x is not None]
    print(f"{sd}: pm10 nonnull={len(pm)} sample={pm[:1]}")
for sd in ["2013-01-01","2015-01-01","2018-01-01","2020-01-01","2021-01-01","2022-01-01","2022-07-29","2022-08-01"]:
    chk(sd)
