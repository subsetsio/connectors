"""Recon: inspect UHERO /category/series response shape for a few categories."""
from subsets_utils import get

BASE = "https://api.uhero.hawaii.edu/v1"
TOKEN = "-VI_yuv0UzZNy4av1SM5vQlkfPK_JKnpGfMzuJR7d0M="
H = {"Authorization": f"Bearer {TOKEN}"}


def fetch(cat):
    r = get(f"{BASE}/category/series", params={"id": cat, "u": "DBEDT", "expand": "true"},
            headers=H, timeout=(10, 120))
    r.raise_for_status()
    return r.json()["data"]


for cat in ["32142", "32134", "32196"]:
    data = fetch(cat)
    print(f"\n===== category {cat}: {len(data) if data else 0} series =====")
    if not data:
        print("  EMPTY")
        continue
    s = data[0]
    print("  series keys:", list(s.keys()))
    print("  sample:", {k: s.get(k) for k in
          ("id", "name", "title", "frequencyShort", "unitsLabel",
           "seasonalAdjustment", "measurementId", "measurementName", "decimals")})
    print("  geography:", s.get("geography"))
    so = s.get("seriesObservations") or {}
    tr = so.get("transformationResults") or []
    print("  transformations:", [t.get("transformation") for t in tr])
    lvl = next((t for t in tr if t.get("transformation") == "lvl"), None)
    if lvl:
        print("  lvl dates[:3]:", lvl.get("dates", [])[:3], "values[:3]:", lvl.get("values", [])[:3])
        print("  lvl len dates/values:", len(lvl.get("dates", [])), len(lvl.get("values", [])))
    # audit across all series in this category
    no_so = sum(1 for x in data if not (x.get("seriesObservations") or {}).get("transformationResults"))
    no_lvl = sum(1 for x in data if not any(
        t.get("transformation") == "lvl"
        for t in ((x.get("seriesObservations") or {}).get("transformationResults") or [])))
    no_geo = sum(1 for x in data if not x.get("geography"))
    freqs = sorted({x.get("frequencyShort") for x in data})
    # check empty/null value cells in lvl arrays
    empties = 0
    total = 0
    for x in data:
        for t in ((x.get("seriesObservations") or {}).get("transformationResults") or []):
            if t.get("transformation") == "lvl":
                for v in t.get("values", []):
                    total += 1
                    if v in (None, "", "NA"):
                        empties += 1
    print(f"  audit: series_no_obs={no_so} series_no_lvl={no_lvl} no_geo={no_geo} freqs={freqs}")
    print(f"  audit: lvl values total={total} empty/null={empties}")
