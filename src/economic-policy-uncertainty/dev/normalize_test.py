import json
from subsets_utils import get
from norm import normalize

files = json.load(open("dev/files.json"))
BASE = "https://www.policyuncertainty.com/media/"

bad = []
for eid, fn in sorted(files.items()):
    url = BASE + fn.replace(" ", "%20")
    try:
        r = get(url, timeout=(10, 120))
        r.raise_for_status()
        df = normalize(r.content, fn)
    except Exception as e:
        bad.append((eid, fn, f"{type(e).__name__}: {e}"))
        print(f"FAIL  {eid:45s} {type(e).__name__}: {e}")
        continue
    n = len(df)
    ns = df["series"].nunique()
    dmin, dmax = df["date"].min(), df["date"].max()
    freqs = sorted(df["frequency"].unique())
    samp = list(df["series"].drop_duplicates().head(3))
    flag = "  <<< LOW" if n < 10 else ""
    print(f"ok    {eid:45s} rows={n:7d} series={ns:4d} {dmin}..{dmax} {freqs} {samp}{flag}")

print(f"\n{len(bad)} failures")
for b in bad:
    print(b)
