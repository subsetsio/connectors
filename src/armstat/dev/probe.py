import sys, json
sys.path.insert(0, "src")
import subsets_utils
captured = {}
def fake_save(rows, asset):
    captured["rows"] = rows; captured["asset"] = asset
    return "memory://"+asset
subsets_utils.save_raw_ndjson = fake_save
import nodes.armstat as m
m.save_raw_ndjson = fake_save
for sid in ["armstat-ef-cpi-mi1", "armstat-tt-tr-fa4", "armstat-af-1-2024"]:
    if sid not in m.ASSET_PATHS:
        print(sid, "NOT IN PATHS"); continue
    captured.clear()
    try:
        m.fetch_one(sid)
        rows = captured["rows"]
        print(f"{sid}: {len(rows)} rows; cols={sorted(rows[0].keys()) if rows else []}")
        print("   sample:", json.dumps(rows[0], ensure_ascii=False) if rows else "none")
        nn = sum(1 for r in rows if r['value'] is not None)
        print(f"   non-null values: {nn}/{len(rows)}")
    except Exception as e:
        import traceback; traceback.print_exc()
