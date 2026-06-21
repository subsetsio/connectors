from subsets_utils import get
import json
countries=[c["alpha3"] for c in get("https://api.climatetrace.org/v6/definitions/countries",timeout=(10,60)).json()]
print("n countries:", len(countries))
import statistics
sizes=[]
sample=countries[::18]  # ~14 sample
for c in sample:
    url=f"https://downloads.climatetrace.org/latest/country_packages/co2e_100yr/{c}.zip"
    r=get(url, headers={"Range":"bytes=0-0"}, timeout=(10,60))
    cr=r.headers.get("content-range","")
    if cr:
        sz=int(cr.split("/")[-1]); sizes.append(sz); print(f"{c}: {sz/1e6:.1f} MB")
avg=statistics.mean(sizes)
print(f"\nsample avg {avg/1e6:.1f} MB, est total {avg*len(countries)/1e9:.1f} GB across {len(countries)} countries")
