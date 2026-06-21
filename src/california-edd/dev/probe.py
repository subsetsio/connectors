import csv, io, json
from subsets_utils import get

BASE = "https://data.ca.gov/api/3"

def pkg_resources(pid):
    r = get(f"{BASE}/action/package_show", params={"id": pid}, timeout=(10, 120))
    r.raise_for_status()
    res = r.json()["result"]["resources"]
    return [(x.get("id"), x.get("format"), x.get("name"), x.get("url")) for x in res]

# CES (3 era CSVs) and QCEW (6 resources) — check schema consistency
for pid, label in [
    ("2a5f872d-f7fe-49f2-9581-8f1b17ce5b90", "CES"),
    ("3f08b68e-1d1a-4ba4-a07d-1ec3392ed191", "QCEW"),
    ("f673ad7c-44ed-4c54-adc7-2f4b23eec557", "RegionalPlanning(gated)"),
]:
    print("====", label, pid)
    for rid, fmt, name, url in pkg_resources(pid):
        print(f"  - {fmt:8} {name[:50]:50} {url}")

# Inspect headers of the CES resources to confirm consistent columns
print("\n=== CES resource headers ===")
for rid, fmt, name, url in pkg_resources("2a5f872d-f7fe-49f2-9581-8f1b17ce5b90"):
    if (fmt or "").upper() != "CSV":
        continue
    resp = get(url, timeout=(10, 180))
    resp.raise_for_status()
    text = resp.text
    rdr = csv.reader(io.StringIO(text))
    header = next(rdr)
    first = next(rdr)
    print(f"  {name}: {len(text)} bytes, {len(header)} cols")
    print("    header:", header)
    print("    row0  :", first)
