import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re
from subsets_utils import get

# 4744 GDP: dynamic, xlsx 404. Check header toolbar for any download url, and pls/ken data.
no = 4744
r = get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl={no}", timeout=(10,60))
cfg = json.loads(r.text)
tb = cfg.get("tableConfig",{}).get("toolbar",{})
print("toolbar:", json.dumps(tb, ensure_ascii=False)[:600])
fields = cfg["tableConfig"]["dataSource"]["fields"]
print("\nfields count:", len(fields.split(",")), "| first:", fields.split(",")[:6])

# data with p_champs, no p_tri
import urllib.parse
u = f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_data?p_id_tabl={no}&p_champs={urllib.parse.quote(fields)}"
d = get(u, timeout=(10,90))
print("\ndata http", d.status_code, "ct", d.headers.get("content-type"), "bytes", len(d.content))
print("first 5 lines:")
for ln in d.text.splitlines()[:5]:
    print("   ", ln[:140])

# A clean tidy dynamic example: 4625 population
print("\n=== 4625 population p_retrn_data (clean) ===")
r2 = get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl=4625", timeout=(10,60))
f2 = json.loads(r2.text)["tableConfig"]["dataSource"]["fields"]
print("fields:", f2.split(","))
d2 = get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_data?p_id_tabl=4625&p_champs={urllib.parse.quote(f2)}", timeout=(10,90))
for ln in d2.text.splitlines()[:4]:
    print("   ", ln[:160])
