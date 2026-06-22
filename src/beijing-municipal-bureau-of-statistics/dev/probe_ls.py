import sys; sys.path.insert(0,"src")
import nodes.beijing_municipal_bureau_of_statistics as M
cap={}
M.save_raw_ndjson=lambda rows,asset:cap.__setitem__(asset,rows)
for eid in ["01-LS-1-07","01-LS-031-001","01-LS-1-08","01-1"]:
    sid=M._spec_id(eid)
    try:
        M.fetch_one(sid); rows=cap.get(sid,[])
        print(f"\n=== {eid}: {len(rows)} rows")
        for r in rows[:6]: print("   ", r)
        # value samples
        vals=[r['value'] for r in rows[:30]]
        print("   value samples:", vals[:12])
    except Exception as e:
        print(f"\n=== {eid}: EXCEPTION {type(e).__name__}: {e}")
