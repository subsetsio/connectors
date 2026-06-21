from subsets_utils import get
# georgia identity
r = get("https://data.berkeleyearth.org/auto/Regional/TAVG/Text/georgia-TAVG-Trend.txt", timeout=(8,30))
for ln in r.text.splitlines()[:6]:
    print("GEORGIA:", repr(ln[:120]))
# TMAX/TMIN regional availability for a few regions
for var in ("TMAX","TMIN"):
    for slug in ("france","california","afghanistan","united-states"):
        u=f"https://data.berkeleyearth.org/auto/Regional/{var}/Text/{slug}-{var}-Trend.txt"
        rr=get(u, timeout=(8,30), headers={"Range":"bytes=0-100"})
        print(var, slug, rr.status_code)
