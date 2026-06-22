import sys; sys.path.insert(0,"src")
import nodes.beijing_municipal_bureau_of_statistics as M
cap={}
M.save_raw_ndjson=lambda rows,asset:cap.__setitem__(asset,rows)
for eid in ["01-LS-1-07","01-LS-031-001","01-LS-1-08","01-60Y-1-03-N","05-DBW-A01","01-1"]:
    sid=M._spec_id(eid)
    try:
        M.fetch_one(sid); rows=cap.get(sid,[])
        nnum=sum(1 for r in rows if r['value'].replace(',','').replace(' ','').replace('.','').replace('-','').isdigit())
        print(f"{eid}: {len(rows)} rows, ~{nnum} numeric-ish")
        if rows: print("   ", rows[0])
    except Exception as e:
        print(f"{eid}: EXC {type(e).__name__}: {e}")
