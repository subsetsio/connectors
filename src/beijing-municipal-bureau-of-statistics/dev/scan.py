import sys, os, json, time
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
os.environ.setdefault("CI","")
import beijing_municipal_bureau_of_statistics as M

captured = {}
M.save_raw_ndjson = lambda rows, asset: captured.__setitem__(asset, len(rows))

ids = list(M._BY_SPEC.keys())
N = int(os.environ.get("SCAN_N", "10"))
START = int(os.environ.get("SCAN_START", "0"))
ids = ids[START:START+N] if N>0 else ids[START:]

out_path = os.environ.get("SCAN_OUT", "dev/scan_result.json")
results = {}
if os.environ.get("SCAN_RESUME") and os.path.exists(out_path):
    results = json.load(open(out_path))

t0=time.time()
for i, sid in enumerate(ids):
    if sid in results:
        continue
    captured.clear()
    try:
        M.fetch_one(sid)
        results[sid] = captured.get(sid, 0)
    except Exception as e:
        results[sid] = f"ERR:{type(e).__name__}:{e}"[:120]
    if (i+1) % 10 == 0:
        json.dump(results, open(out_path,"w"), ensure_ascii=False)
        print(f"  {i+1}/{len(ids)} done, {time.time()-t0:.1f}s elapsed", flush=True)
json.dump(results, open(out_path,"w"), ensure_ascii=False)
empties=[k for k,v in results.items() if v==0]
errs=[k for k,v in results.items() if isinstance(v,str)]
print(f"DONE {len(results)} entities in {time.time()-t0:.1f}s | empty(0 rows)={len(empties)} | errors={len(errs)}")
print("avg sec/entity:", (time.time()-t0)/max(1,len(ids)))
