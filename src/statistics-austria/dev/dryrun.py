import sys, csv, io, re, json
sys.path.insert(0, 'src')
# import the helpers but stub save_raw_ndjson to capture
import nodes.statistics_austria as m

captured = {}
def fake_save(rows, asset):
    captured[asset] = rows
m.save_raw_ndjson = fake_save

for eid in ["OGD_krebs_ext_KREBS_1", "OGDEXT_AEST_GEMTAB_1", "OGDEXT_VORNAMEN_1"]:
    nid = f"statistics-austria-{eid.lower().replace('_','-')}"
    try:
        m.fetch_one(nid)
        rows = captured[nid]
        print(f"\n### {eid}  ({len(rows)} rows)")
        print("cols:", list(rows[0].keys()))
        for r in rows[:3]:
            print("  ", json.dumps(r, ensure_ascii=False)[:240])
    except Exception as e:
        print(f"\n### {eid} FAILED: {type(e).__name__}: {e}")
