from subsets_utils import get, post

info = get("https://api.statbank.dk/v1/tableinfo/ABST1?format=JSON&lang=en").json()
variables = [{"code": v["id"], "values": ["*"]} for v in info["variables"]]

# POST with lang=en in body
body = {"table": "ABST1", "format": "BULK", "lang": "en", "variables": variables}
r = post("https://api.statbank.dk/v1/data", json=body)
print("=== lang=en in body ===", r.status_code)
print(r.text[:400])

# try streaming a bigger table to see size; use stream + iter_lines
print("\n=== FOLK1A info ===")
info2 = get("https://api.statbank.dk/v1/tableinfo/FOLK1A?format=JSON&lang=en").json()
ncells = 1
for v in info2["variables"]:
    print("  var", v["id"], len(v["values"]))
    ncells *= len(v["values"])
print("approx cells:", ncells)
