import subsets_utils

captured = {}
subsets_utils.save_raw_ndjson = lambda rows, asset, **k: captured.__setitem__(asset, list(rows))

import importlib.util, sys, pathlib
p = pathlib.Path(__file__).resolve().parents[1] / "src" / "nodes" / "freedom_house.py"
spec = importlib.util.spec_from_file_location("fh", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

for s in m.DOWNLOAD_SPECS:
    s.fn(s.id)
    rows = captured[s.id]
    print("=" * 70)
    print(s.id, "->", len(rows), "rows")
    if rows:
        yrs = sorted({r.get("year") for r in rows if r.get("year") is not None})
        print("  years:", yrs[0], "..", yrs[-1], f"({len(yrs)} distinct)")
        print("  cols:", list(rows[0].keys()))
        print("  sample:", {k: rows[0][k] for k in list(rows[0])[:8]})
        # null check on a key numeric per asset
        print("  last:", {k: rows[-1][k] for k in list(rows[-1])[:8]})
