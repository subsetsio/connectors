import sys, itertools
sys.path.insert(0, "src")
from nodes import afdb as m

did = "salbpsf"  # SDG progress, ~52 series, small
meta = m._get(f"/meta/dataset/{did}")
dims = meta["dimensions"]
print("dims:", [d["id"] for d in dims])
mbd = {d["id"]: m._dimension_members(did, d["id"]) for d in dims}
print("member counts:", {k: len(v) for k, v in mbd.items()})
freq = m._detect_frequency(did, dims, mbd)
print("detected native freq:", freq)
keys = {d: [x["key"] for x in mbd[d]] for d in mbd}
rows = list(itertools.islice(m._iter_rows(did, dims, keys, freq), 3))
print("sample raw row dims:", {k: rows[0][k] for k in rows[0] if isinstance(rows[0][k], dict)})
print("freq/start/nvals:", rows[0]["frequency"], rows[0]["startDate"][:10], len(rows[0]["values"]))
recs = list(m._expand(rows[0], dims))
print("expanded count:", len(recs))
print("sample expanded recs:")
for r in recs[:3]:
    print("  ", r)
