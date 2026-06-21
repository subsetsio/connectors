import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

B = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"

def g(path):
    r = get(B + path, timeout=(10, 120))
    r.raise_for_status()
    return r.json()

# 1. Does compareBy change the returned key set, or is it always the full combo grid?
def keyset(site, dt, gt, cmp):
    d = g(f"render_region_5.php?site={site}&data_type={dt}&graph_type={gt}&compareBy={cmp}")
    if isinstance(d, str):
        d = json.loads(d)
    return d

print("=== region_3 for site=1 dt=1 gt=2 (recent trends): compareBy options ===")
r3 = g("render_region_3_controls.php?site=1&data_type=1&graph_type=2")
cv = r3["CheckboxValues"]
for f, spec in cv.items():
    print(" ", f, "AllowAsCompareBy=", spec.get("AllowAsCompareBy"), "values=", spec.get("values"))

print("\n=== render_region_5 compareBy=sex (site=1 dt=1 gt=2) ===")
d_sex = keyset(1, 1, 2, "sex")
print("info:", json.dumps(d_sex["info"], indent=0)[:600])
ks = list(d_sex["data"].keys())
print("n keys:", len(ks), "sample:", ks[:8])
print("sample series first row:", d_sex["data"][ks[0]]["data_series"][:2])

print("\n=== compareBy=race ===")
d_race = keyset(1, 1, 2, "race")
kr = list(d_race["data"].keys())
print("n keys:", len(kr), "sample:", kr[:8])
print("keyset equal to sex?", set(ks) == set(kr))

print("\n=== compareBy=site? (does it return all sites in one call) ===")
try:
    d_site = keyset(1, 1, 2, "site")
    kk = list(d_site["data"].keys())
    sites_in = set(k.split("_")[-1] for k in kk)
    print("n keys:", len(kk), "distinct site codes in keys:", sorted(sites_in)[:20], "count:", len(sites_in))
except Exception as e:
    print("site compareBy err:", e)

print("\n=== different site (breast=55) returns its own data ===")
d55 = keyset(55, 1, 2, "sex")
k55 = list(d55["data"].keys())
print("n keys:", len(k55), "sample:", k55[:5], "site codes:", set(k.split("_")[-1] for k in k55))
