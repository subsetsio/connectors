import json
from subsets_utils import get

def J(url):
    return get(url, timeout=(10,120))

# FNYR - is it flat or nested?
d = J("https://data.financialresearch.gov/v1/series/dataset/?dataset=FNYR").json()
ts = d["timeseries"]; k0 = next(iter(ts))
print("FNYR top:", list(d.keys()), "nseries", len(ts))
print("FNYR series keys:", list(ts[k0].keys()))
print("FNYR inner timeseries keys:", list(ts[k0]["timeseries"].keys()))
print("FNYR metadata keys:", list(ts[k0]["metadata"].keys()))
print("FNYR metadata sample:", json.dumps(ts[k0]["metadata"], default=str)[:600])

# HFM FPF
d2 = J("https://data.financialresearch.gov/hf/v1/series/dataset/?dataset=fpf").json()
ts2 = d2["timeseries"]; k2 = next(iter(ts2))
print("\nFPF top:", list(d2.keys()), "nseries", len(ts2))
print("FPF series keys:", list(ts2[k2].keys()))
print("FPF inner timeseries keys:", list(ts2[k2]["timeseries"].keys()))
print("FPF agg head:", json.dumps(ts2[k2]["timeseries"].get("aggregation", "NONE"), default=str)[:200])

# FSI CSV
r = get("https://www.financialresearch.gov/financial-stress-index/data/fsi.csv", timeout=(10,120))
print("\nFSI status", r.status_code, "ctype", r.headers.get("content-type"))
lines = r.text.splitlines()
print("FSI nlines", len(lines))
print("FSI header:", lines[0])
print("FSI row1:", lines[1]); print("FSI last:", lines[-1])
