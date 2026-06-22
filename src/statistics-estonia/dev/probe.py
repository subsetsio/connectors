import json
from subsets_utils import get, post

ROOT = "https://andmed.stat.ee/api/v1/en/stat"
path = "rahvastik/rahvastikunaitajad-ja-koosseis/demograafilised-pehinaitajad/RV030.PX"
url = ROOT + "/" + path

# 1. metadata
meta = get(url, timeout=(10, 60)).json()
print("=== META keys:", list(meta.keys()))
print("title:", meta.get("title"))
for v in meta["variables"]:
    print("  var:", v.get("code"), "| text:", v.get("text"),
          "| nvalues:", len(v.get("values", [])),
          "| time:", v.get("time"), "| elim:", v.get("elimination"))

# 2. build full query
query = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}}
         for v in meta["variables"]]
body = {"query": query, "response": {"format": "json-stat2"}}
r = post(url, json=body, timeout=(10, 120))
print("=== DATA status:", r.status_code)
data = r.json()
print("data top keys:", list(data.keys()))
print("class:", data.get("class"))
print("dim ids (id):", data.get("id"))
print("size:", data.get("size"))
print("value len:", len(data.get("value", [])))
print("value sample:", data.get("value", [])[:8])
dims = data.get("dimension", {})
for did in data.get("id", []):
    d = dims[did]
    cat = d.get("category", {})
    idx = cat.get("index"); lab = cat.get("label")
    print(f"  DIM {did} label={d.get('label')!r} ncat={len(idx) if idx else '?'}")
    # show first couple categories
    if isinstance(idx, dict):
        items = sorted(idx.items(), key=lambda kv: kv[1])[:3]
    elif isinstance(idx, list):
        items = [(k, i) for i, k in enumerate(idx)][:3]
    else:
        items = []
    for code, i in items:
        print("      ", code, "->", (lab or {}).get(code))
