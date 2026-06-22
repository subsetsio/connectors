from subsets_utils import get
BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

# quarterly label format
r = get(f"{BASE}/PN02526AQ/json/2000-1/2026-4", timeout=(10,120)).json()
print("quarterly title", r["config"]["title"])
print("quarterly periods", [p["name"] for p in r["periods"][:6]], "...", r["periods"][-1]["name"])

# annual label
r = get(f"{BASE}/PM05317AA/json/2000/2026", timeout=(10,120)).json()
print("annual periods", [p["name"] for p in r["periods"][:4]], "...", r["periods"][-1]["name"])

# monthly month tokens across a full year span
r = get(f"{BASE}/PN00001MM/json/2023-1/2024-12", timeout=(10,120)).json()
print("monthly tokens", [p["name"] for p in r["periods"]])

# daily tokens across months
r = get(f"{BASE}/PD04637PD/json/2025-1-1/2025-12-31", timeout=(10,120)).json()
labs = [p["name"] for p in r["periods"]]
print("daily first/last", labs[:3], labs[-3:], "n", len(labs))
# unique month tokens in daily
import re
toks = sorted(set(l.split(".")[1] for l in labs))
print("daily month toks", toks)
