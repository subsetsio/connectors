import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

B = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"

def g(path):
    r = get(B + path, timeout=(10, 120))
    r.raise_for_status()
    d = r.json()
    return json.loads(d) if isinstance(d, str) else d

def cmp_for(site, dt, gt):
    r3 = get(B + f"render_region_3_controls.php?site={site}&data_type={dt}&graph_type={gt}", timeout=(10,120))
    r3.raise_for_status()
    cv = r3.json().get("CheckboxValues", {})
    for f, spec in cv.items():
        if spec.get("AllowAsCompareBy") and f != "site":
            return f, list(cv.keys())
    return (list(cv.keys())[0] if cv else None), list(cv.keys())

def show(site, dt, gt, name):
    cb, fields = cmp_for(site, dt, gt)
    print(f"\n=== {name}: site={site} dt={dt} gt={gt} compareBy={cb} fields={fields} ===")
    d = g(f"render_region_5.php?site={site}&data_type={dt}&graph_type={gt}&compareBy={cb}")
    info = d["info"]
    print("  x-axis:", info.get("x-axis"), "| y-axis:", info.get("y-axis"))
    print("  key-order:", info.get("key-order"))
    print("  data-fields:", info.get("data-fields"))
    print("  trend-fields:", info.get("trend-fields"))
    k0 = next(iter(d["data"]))
    entry = d["data"][k0]
    print("  data[key] keys:", list(entry.keys()))
    print("  sample key:", k0, "first 2 series rows:", entry.get("data_series", [])[:2])
    for tk in entry:
        if tk != "data_series":
            print("   extra series", tk, "->", entry[tk][:2] if isinstance(entry[tk], list) else entry[tk])

# incidence recent trends (year x-axis, rate)
show(1, 1, 2, "SEER Incidence Recent Trends")
# survival 5-year (dt4 gt5)
show(1, 4, 5, "Survival 5-Year")
# median age (dt1 gt14)
show(1, 1, 14, "SEER Incidence Median Age")
# stage distribution (dt1 gt4)
show(60, 1, 4, "Stage Distribution")
# prevalence complete (dt5 gt11)
show(1, 5, 11, "Prevalence Complete")
# risk intervals (dt6 gt8)
show(1, 6, 8, "Risk Intervals")
# survival by time since dx (dt4 gt6)
show(1, 4, 6, "Survival By Time Since Dx")

# invalid combo behavior: region_3 for a site that lacks the combo
print("\n=== invalid combo region_3 (mortality rural/urban at a tiny site) ===")
try:
    r = get(B + "render_region_3_controls.php?site=63&data_type=2&graph_type=15", timeout=(10,120))
    print("status", r.status_code, "body head:", r.text[:120])
except Exception as e:
    print("err", e)
