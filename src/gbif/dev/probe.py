import json
from subsets_utils import get

BASE = "https://api.gbif.org/v1"


def facet(endpoint, fc, extra=None, fl=2000):
    params = {"limit": 0, "facet": fc, "facetLimit": fl}
    if extra:
        params.update(extra)
    r = get(f"{BASE}/{endpoint}", params=params, timeout=(10.0, 120.0))
    r.raise_for_status()
    d = r.json()
    fs = d.get("facets", [])
    counts = fs[0].get("counts", []) if fs else []
    return d.get("count"), counts


# single facet: year
tot, counts = facet("occurrence/search", "year")
print("YEAR total:", tot, "distinct:", len(counts), "sample:", counts[:3])

# single facet: publishingCountry
tot, counts = facet("occurrence/search", "publishingCountry")
print("PUBCOUNTRY distinct:", len(counts), "sample:", counts[:3])

# panel: enumerate countries, then year facet for one country
_, ccounts = facet("occurrence/search", "country")
print("COUNTRY distinct:", len(ccounts), "sample names:", [c["name"] for c in ccounts[:5]])
one = ccounts[0]["name"]
_, yc = facet("occurrence/search", "year", extra={"country": one})
print(f"YEAR facet filtered country={one}: distinct {len(yc)} sample {yc[:3]}")

# kingdomKey enumeration
_, kc = facet("occurrence/search", "kingdomKey")
print("KINGDOM keys:", [c["name"] for c in kc])

# basisOfRecord
_, bc = facet("occurrence/search", "basisOfRecord")
print("BASIS values:", [c["name"] for c in bc])

# issue / license
_, ic = facet("occurrence/search", "issue")
print("ISSUE distinct:", len(ic), "sample:", [c["name"] for c in ic[:5]])
_, lc = facet("occurrence/search", "license")
print("LICENSE:", [(c["name"], c["count"]) for c in lc])

# dataset registry facets
tot, tc = facet("dataset/search", "type")
print("DATASET total:", tot, "types:", [(c["name"], c["count"]) for c in tc])
tot, dpc = facet("dataset/search", "publishingCountry")
print("DATASET pubcountry distinct:", len(dpc), "sample:", [c["name"] for c in dpc[:3]])
