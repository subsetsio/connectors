import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

B = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"

def _raw(path):
    r = get(B + path, timeout=(10, 120))
    return r

def gj(path):
    r = _raw(path); r.raise_for_status()
    d = r.json()
    return json.loads(d) if isinstance(d, str) else d

VF = gj("get_var_formats.php")
FMT = VF["VariableFormats"]
SITES = [str(s["value"]) if isinstance(s, dict) else str(s) for s in VF["CancerSites"]]

def num(v):
    if v is None: return None
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return v
    s = str(v).strip()
    if s == "": return None
    try:
        return int(s)
    except ValueError:
        try: return float(s)
        except ValueError: return s

def decode(field, code):
    table = FMT.get(field)
    if isinstance(table, dict):
        return table.get(str(code), str(code))
    return str(code)

def compare_by_for(site, dt, gt):
    r = _raw(f"render_region_3_controls.php?site={site}&data_type={dt}&graph_type={gt}")
    if r.status_code != 200: return None
    cv = r.json().get("CheckboxValues", {})
    for f, spec in cv.items():
        if spec.get("AllowAsCompareBy") and f != "site":
            return f
    return next(iter(cv), None)

def flatten_site(dt, gt, site, cb):
    r = _raw(f"render_region_5.php?site={site}&data_type={dt}&graph_type={gt}&compareBy={cb}")
    if r.status_code != 200:
        return None, r.status_code
    d = r.json()
    if isinstance(d, str): d = json.loads(d)
    info = d.get("info", {})
    ko = info.get("key-order", [])
    df = info.get("data-fields", [])
    rows = []
    for key, entry in d.get("data", {}).items():
        codes = key.split("_")
        dims = {ko[i]: decode(ko[i], codes[i]) for i in range(min(len(ko), len(codes)))}
        for series_row in entry.get("data_series", []):
            rec = dict(dims)
            for i, fld in enumerate(df):
                rec[fld] = num(series_row[i]) if i < len(series_row) else None
            rows.append(rec)
    return rows, 200

# Test entity seer-incidence-recent-trends (dt1 gt2) on 2 sites
dt, gt = "1", "2"
cb = compare_by_for("1", dt, gt)
print("compareBy:", cb)
for site in ["1", "55"]:
    rows, st = flatten_site(dt, gt, site, cb)
    print(f"site {site}: status {st}, rows {len(rows) if rows else 0}; sample:", rows[0] if rows else None)

# Test an invalid-ish combo: mortality rural-urban (dt2 gt15) on small site 63
dt, gt = "2", "15"
cb = compare_by_for("1", dt, gt) or "sex"
print("\nmortality rural-urban compareBy:", cb)
for site in ["1", "63", "47"]:
    rows, st = flatten_site(dt, gt, site, cb)
    print(f"site {site}: status {st}, rows {len(rows) if rows else 0}")

# survival 5yr sample
dt, gt = "4", "5"; cb = compare_by_for("1", dt, gt)
rows, st = flatten_site(dt, gt, "55", cb)
print("\nsurvival5yr breast compareBy", cb, "rows", len(rows), "sample:", rows[0] if rows else None)
