import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.environ.pop("CI", None)  # local dev write to data/dev
import importlib
mod = importlib.import_module("nodes.ca_qc_isq")
from subsets_utils import load_raw_parquet

# pick a static, a dynamic, and a couple random union ids
test_ids = [
    "ca-qc-isq-person-years-wage-bill-and-paid-hours-for-core-drilling-quebec",  # static
    "ca-qc-isq-gross-domestic-product-expenditure-quebec",                       # dynamic
]
# add 3 from constants
test_ids += [s.id for s in mod.DOWNLOAD_SPECS[:3]]
for sid in test_ids:
    if sid not in mod.SPEC_TO_SLUG:
        print("SKIP (not a real spec):", sid); continue
    try:
        mod.fetch_one(sid)
        t = load_raw_parquet(sid)
        print(f"OK  {sid[:55]:55} rows={t.num_rows:>6} cols={t.column_names}")
    except Exception as e:
        import traceback; traceback.print_exc()
        print("FAIL", sid, type(e).__name__, e)
