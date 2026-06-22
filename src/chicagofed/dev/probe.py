import sys
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
from constants import ENTITY_IDS, PERIOD_COL_OVERRIDES
import importlib.util
spec = importlib.util.spec_from_file_location("cf", "src/nodes/chicagofed.py")
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)

for eid in ENTITY_IDS:
    provider, stem = eid.split("/", 1)
    url = f"{cf.DATA_BASE}/{provider}/{stem}.csv"
    text = cf._fetch_csv(url)
    rows = cf._parse_long(text, PERIOD_COL_OVERRIDES.get(eid))
    series = sorted({r["series"] for r in rows})
    sample = rows[0] if rows else None
    print(f"{eid:55s} rows={len(rows):6d} nseries={len(series):2d} sample={sample}")
