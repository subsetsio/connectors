import sys, os, json, tempfile
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
os.environ.setdefault("CI","")  # local dev mode
import beijing_municipal_bureau_of_statistics as M

# monkeypatch save_raw_ndjson to capture
captured = {}
def fake_save(rows, asset):
    captured[asset] = rows
M.save_raw_ndjson = fake_save

for sid in ["beijing-municipal-bureau-of-statistics-01-ls-1-07",
            "beijing-municipal-bureau-of-statistics-01-ls-1-08",
            "beijing-municipal-bureau-of-statistics-01-ls-031-001",
            "beijing-municipal-bureau-of-statistics-01-1"]:
    try:
        M.fetch_one(sid)
        rows = captured.get(sid, [])
        print(f"{sid}: {len(rows)} rows")
        if rows: print("   sample:", json.dumps(rows[0], ensure_ascii=False))
    except Exception as e:
        print(f"{sid}: ERROR {type(e).__name__}: {e}")
