import sys, json, traceback
sys.path.insert(0, "src")
import nodes.alaska_department_of_labor_and_workforce_development as m

captured = {}
def fake_save(rows, asset_id, **kw):
    captured[asset_id] = rows
m.save_raw_ndjson = fake_save

for spec in m.DOWNLOAD_SPECS:
    e = spec.id.replace(m.SLUG + "-", "")
    try:
        spec.fn(spec.id)
        rows = captured.get(spec.id, [])
        n = len(rows)
        cols = sorted(rows[0].keys()) if rows else []
        nonnull = {}
        if rows:
            for k in rows[0]:
                nn = sum(1 for r in rows if r.get(k) is not None)
                nonnull[k] = nn
        print(f"\n### {e}: {n} rows")
        print("  cols:", cols)
        if rows:
            print("  sample:", json.dumps(rows[0], default=str)[:300])
            print("  sample_mid:", json.dumps(rows[n//2], default=str)[:300])
            # flag all-null columns
            allnull = [k for k, v in nonnull.items() if v == 0]
            if allnull:
                print("  ALL-NULL COLS:", allnull)
    except Exception as ex:
        print(f"\n### {e}: ERROR {type(ex).__name__}: {ex}")
        traceback.print_exc()
