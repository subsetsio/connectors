import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from nodes.central_bank_of_malta import _download, _quote_path, parse_workbook, ENTITY_PATHS

for eid in ["balsheetcbm", "inflation-hicp", "fsi-core-banks"]:
    path = ENTITY_PATHS[eid]
    ext = path.rsplit(".", 1)[-1].lower()
    try:
        content = _download(_quote_path(path))
        rows = parse_workbook(content, ext)
        print(f"{eid}: {len(content)} bytes, {len(rows)} rows; sample={rows[0] if rows else None}")
    except Exception as e:
        print(f"{eid}: ERROR {type(e).__name__}: {e}")
