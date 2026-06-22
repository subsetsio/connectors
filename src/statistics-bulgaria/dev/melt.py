import sys, os, math, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json as _json
from subsets_utils import get

def fetch_json(id):
    raw = get(f"https://www.nsi.bg/opendata/getopendata_json.php?l=en&id={id}", timeout=(10,120)).content
    for enc in ("utf-8-sig","utf-8","cp1251","cp1252","latin-1"):
        try:
            return _json.loads(raw.decode(enc))
        except (UnicodeDecodeError, _json.JSONDecodeError):
            continue
    raise ValueError("could not decode JSON-stat")

def sanitize(name, used):
    s = re.sub(r'[^0-9a-zA-Z]+', '_', name.strip().lower()).strip('_')
    if not s: s = "dim"
    if s[0].isdigit(): s = "d_" + s
    base = s; i = 2
    while s in used:
        s = f"{base}_{i}"; i += 1
    used.add(s); return s

def positions(dim):
    cat = dim["category"]
    idx = cat.get("index"); lab = cat.get("label") or {}
    if isinstance(idx, dict):
        order = [c for c,_ in sorted(idx.items(), key=lambda kv: kv[1])]
    elif isinstance(idx, list):
        order = list(idx)
    else:
        order = list(lab.keys())
    labels = [lab.get(c, c) for c in order]
    return order, labels

def melt(d):
    ids = d["id"]; sizes = d["size"]; dim = d["dimension"]
    role = d.get("role") or {}
    time_dims = set(role.get("time") or [])
    metric_dims = set(role.get("metric") or [])
    # strides row-major
    strides = [1]*len(sizes)
    for i in range(len(sizes)-2, -1, -1):
        strides[i] = strides[i+1]*sizes[i+1]
    pos = {dk: positions(dim[dk]) for dk in ids}
    # column assignment
    used = set(["period","unit","value"])
    colmap = {}  # dk -> column name
    period_dim = None; unit_dim = None
    for dk in ids:
        if dk in time_dims and period_dim is None:
            period_dim = dk; continue
        if dk in metric_dims and unit_dim is None:
            unit_dim = dk; continue
        colmap[dk] = sanitize(dim[dk].get("label") or dk, used)
    values = d["value"]
    rows = []
    n = math.prod(sizes) if sizes else 0
    for p in range(n):
        v = values[p] if p < len(values) else None
        if v is None: continue
        if isinstance(v, str):
            v = v.strip()
            if v in ("", "..", ":", "-", "...", "."): continue
            try: v = float(v.replace(",", ""))
            except ValueError: continue
        row = {}
        for i, dk in enumerate(ids):
            cidx = (p // strides[i]) % sizes[i]
            code, label = pos[dk][0][cidx], pos[dk][1][cidx]
            if dk == period_dim: row["period"] = code
            elif dk == unit_dim: row["unit"] = label
            else: row[colmap[dk]] = label
        row["value"] = float(v)
        rows.append(row)
    cols = (["period"] if period_dim else []) + list(colmap.values()) + (["unit"] if unit_dim else []) + ["value"]
    return rows, cols

for id in (1363, 1103, 1942, 301, 612, 818, 1678, 1893, 2636):
    d = fetch_json(id)
    rows, cols = melt(d)
    print(f"id={id} label={d.get('label')[:40]!r} cols={cols} nrows={len(rows)}")
    if rows: print("   sample:", rows[0])
