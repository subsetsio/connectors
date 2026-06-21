import io, pandas as pd
from subsets_utils import get

BASE = "https://ckan.publishing.service.gov.uk/api/3/action"

def pkg(uid):
    r = get(f"{BASE}/package_show", params={"id": uid}, timeout=(10,120))
    r.raise_for_status()
    return r.json()["result"]

# petrol & diesel (single xlsx), ambient gamma (csv)
for uid in ["21db6396-3daf-4d90-8b3f-054995256018", "4f5d442f-a5ae-4865-8e51-091d0a4d2324"]:
    p = pkg(uid)
    res = p["resources"]
    fmts = {}
    for r in res:
        f = (r.get("format") or "").lower().lstrip(".")
        fmts.setdefault(f, 0); fmts[f]+=1
    print("===", p["name"], "nres", len(res), "fmts", fmts)
    # grab first tabular resource
    tab = [r for r in res if (r.get("format") or "").lower().lstrip(".") in ("csv","xlsx","xls","ods")]
    print("  first tabular:", tab[0]["format"], tab[0]["url"])

# parse the petrol xlsx
p = pkg("21db6396-3daf-4d90-8b3f-054995256018")
url = [r for r in p["resources"] if (r.get("format") or "").lower().lstrip(".")=="xlsx"][0]["url"]
b = get(url, timeout=(10,180)).content
print("xlsx bytes", len(b))
xl = pd.ExcelFile(io.BytesIO(b))
print("sheets:", xl.sheet_names)
for sn in xl.sheet_names[:2]:
    df = pd.read_excel(xl, sheet_name=sn, header=None, nrows=8)
    print(f"--- sheet {sn} shape(head)={df.shape}")
    print(df.to_string(max_cols=8))
