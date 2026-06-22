import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
# import the production module and exercise the fallback decision + freq fetch
# WITHOUT touching the production raw layer (write to a temp duckdb-free check).
import httpx
import importlib.util
spec = importlib.util.spec_from_file_location("bbmod", os.path.join(os.path.dirname(__file__),"..","src","nodes","bundesbank.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("module imports OK; DOWNLOAD_SPECS", len(m.DOWNLOAD_SPECS), "TRANSFORM_SPECS", len(m.TRANSFORM_SPECS))
print("FREQ_CODES", m.FREQ_CODES)

# 1) confirm whole-flow BBBK7 raises 413 (so fallback triggers)
try:
    m._fetch_dataflow("__scratch_bbbk7_whole", "BBBK7")
    print("UNEXPECTED: whole-flow returned without 413")
except httpx.HTTPStatusError as e:
    print("whole-flow status:", e.response.status_code, "(413 -> fallback)")

# 2) confirm a 404 frequency is correctly classified (e.g. A has no data)
import importlib
# test _fetch_freq on freq 'M' (404 expected) -> should raise 404 (not retried forever)
try:
    n = m._fetch_freq("__scratch_bbbk7_M", "BBBK7", "M")
    print("freq M rows:", n)
except httpx.HTTPStatusError as e:
    print("freq M status:", e.response.status_code, "(404 -> skipped)")
