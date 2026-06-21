import sys
sys.path.insert(0,'src'); sys.path.insert(0,'src/nodes')
import idb
import pyarrow.parquet as pq, glob

# 1) Excel path: freight yearbook (only XLSM)
nid="idb-freight-transport-and-logistics-statistics-yearbook-2012-2014"
print("=== freight XLSM", flush=True)
try:
    idb.fetch_one(nid)
    for f in glob.glob("data/**/idb-freight-transport-and-logistics-statistics-yearbook-2012-2014.parquet", recursive=True):
        t=pq.read_table(f); print("rows:", t.num_rows, "cols:", t.column_names[:8], "...", flush=True)
except Exception as e:
    print("FREIGHT ERR:", type(e).__name__, str(e)[:200], flush=True)

# 2) Probe-only dominant-group check on social-indicators (no big download)
print("\n=== social-indicators probe/group ===", flush=True)
rec=idb._api("package_show", id="social-indicators-of-latin-america-and-the-caribbean")
probes=[]
for rr in rec["resources"]:
    p=idb._probe_resource(rr) if rr.get("datastore_active") else None
    if p: probes.append(p)
groups={}
for p in probes: groups.setdefault(p["cols"],[]).append(p)
ranked=sorted(groups.items(), key=lambda kv:-sum(x["weight"] for x in kv[1]))
print("n groups:", len(groups), "n probes:", len(probes), flush=True)
for cols,members in ranked[:4]:
    print(f"  weight={sum(x['weight'] for x in members):>10} nres={len(members):>3} ncols={len(cols)} sample_cols={list(cols)[:5]}", flush=True)
