from subsets_utils import get
BASE = "https://www.smard.de/app/chart_data"

def chunks(f, r, res):
    resp = get(f"{BASE}/{f}/{r}/index_{res}.json", timeout=(10,60))
    if resp.status_code != 200: return None
    return resp.json().get("timestamps", [])

def series(f, r, res, t):
    resp = get(f"{BASE}/{f}/{r}/{f}_{r}_{res}_{t}.json", timeout=(10,60))
    if resp.status_code != 200: return None
    return resp.json()["series"]

def summary(f, r, res="day", label=""):
    ts = chunks(f, r, res)
    if not ts:
        print(f"  {label} {f}/{r}: NO INDEX"); return
    # last chunk (most recent year)
    s = series(f, r, res, ts[-1])
    nonnull = [v for _, v in s if v is not None]
    samp = [(p[0], p[1]) for p in s if p[1] is not None][:2]
    print(f"  {label} {f}/{r}/{res}: chunks={len(ts)} lastchunk_points={len(s)} nonnull={len(nonnull)} sample={samp}")

print("generation day (DE + control zones):")
for r in ["DE","50Hertz","TransnetBW","AT"]:
    summary("4068", r, "day", "PV")
summary("1224","DE","day","Nuclear")
print("consumption day:")
for f in ["410","4359","4387"]:
    summary(f,"DE","day")
print("forecast day:")
for f in ["122","3791","125"]:
    summary(f,"DE","day")
print("prices day (region DE-LU):")
for f in ["4169","5078","4170","252","255","256","4996"]:
    summary(f,"DE-LU","day")
print("prices day (other regions for neighbor zones):")
for f,r in [("4170","AT"),("252","DE-LU")]:
    summary(f,r,"day")
