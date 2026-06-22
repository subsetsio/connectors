from subsets_utils import get

URLS = {
    "global_land_ocean": "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt",
    "global_tavg": "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_complete.txt",
    "us_tavg": "https://data.berkeleyearth.org/auto/Regional/TAVG/Text/united-states-TAVG-Trend.txt",
    "france_tmax": "https://data.berkeleyearth.org/auto/Regional/TMAX/Text/france-TMAX-Trend.txt",
    "california_tmin": "https://data.berkeleyearth.org/auto/Regional/TMIN/Text/california-TMIN-Trend.txt",
}

for name, url in URLS.items():
    try:
        r = get(url, timeout=(10.0, 120.0))
        print(f"\n===== {name} | {url}")
        print("status", r.status_code, "len", len(r.text))
        lines = r.text.splitlines()
        print("total lines", len(lines))
        ncomment = sum(1 for ln in lines if ln.startswith("%"))
        print("comment lines", ncomment)
        for ln in lines[:60]:
            print(repr(ln[:160]))
        print("... first data lines ...")
        data_lines = [ln for ln in lines if ln and not ln.startswith("%")]
        for ln in data_lines[:5]:
            print(repr(ln[:200]))
        print("... last data lines ...")
        for ln in data_lines[-3:]:
            print(repr(ln[:200]))
    except Exception as e:
        print(f"\n===== {name} | {url} ERROR {type(e).__name__}: {e}")
