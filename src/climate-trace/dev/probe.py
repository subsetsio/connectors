import sys, io, zipfile, tempfile, csv
from subsets_utils import get, get_client

BASE = "https://downloads.climatetrace.org/latest/sector_packages"
GAS = "co2e_100yr"
SECTORS = ["agriculture","buildings","fluorinated-gases","forestry-and-land-use",
           "fossil-fuel-operations","manufacturing","mineral-extraction","power",
           "transportation","waste"]

# 1) which sectors have a co2e_100yr sector package?
print("=== availability ===")
avail=[]
for s in SECTORS:
    url=f"{BASE}/{GAS}/{s}.zip"
    r=get(url, headers={"Range":"bytes=0-0"}, timeout=(10,60))
    cr=r.headers.get("content-range","")
    size=cr.split("/")[-1] if cr else "?"
    ok = r.status_code in (200,206)
    if ok: avail.append(s)
    print(f"{s:28} {r.status_code} size={size}")

# 2) stream-download smallest (power), extract member types
print("\n=== stream power.zip and inspect members ===")
url=f"{BASE}/{GAS}/power.zip"
tmp=tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
with get_client().stream("GET", url, timeout=(10,300)) as resp:
    resp.raise_for_status()
    for chunk in resp.iter_bytes(1<<20):
        tmp.write(chunk)
tmp.close()
zf=zipfile.ZipFile(tmp.name)
names=zf.namelist()
ce=[n for n in names if n.endswith(".csv") and "_country_emissions_" in n]
es=[n for n in names if n.endswith(".csv") and "_emissions_sources_" in n and "_confidence_" not in n]
print("total members:", len(names))
print("country_emissions members:", len(ce), ce[:3])
print("emissions_sources members:", len(es), es[:3])
# headers + a couple rows + gas distinct
import collections
if ce:
    with zf.open(ce[0]) as f:
        rdr=csv.reader(io.TextIOWrapper(f,encoding="utf-8"))
        hdr=next(rdr); print("\nCE header:", hdr)
        rows=[next(rdr) for _ in range(2)]
        for r in rows: print("CE row:", r)
if es:
    with zf.open(es[0]) as f:
        rdr=csv.reader(io.TextIOWrapper(f,encoding="utf-8"))
        hdr=next(rdr); print("\nES header (first 22):", hdr[:22])
        r=next(rdr); print("ES row (first 22):", r[:22])
print("\navailable sectors:", avail)
