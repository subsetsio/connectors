import sys, json, time
sys.path.insert(0, "src")
# import production logic
import importlib.util
spec = importlib.util.spec_from_file_location("elstat_node", "src/nodes/elstat.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

from constants import ENTITY_IDS
from concurrent.futures import ThreadPoolExecutor, as_completed

def check(code):
    try:
        files = mod._select_excel(mod._excel_attachments(code))
        rows = []
        for fn, content in files:
            rows.extend(mod._melt_workbook(content, fn))
        return code, len(files), len(rows), None
    except Exception as e:
        return code, -1, -1, f"{type(e).__name__}: {e}"

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(check, c): c for c in ENTITY_IDS}
    for i, fut in enumerate(as_completed(futs)):
        code, nf, nr, err = fut.result()
        results[code] = (nf, nr, err)
        if err or nr == 0:
            print(f"  [{i+1}/{len(ENTITY_IDS)}] {code}: files={nf} rows={nr} err={err}", flush=True)

empty = sorted([c for c,(nf,nr,err) in results.items() if (err is None and nr==0)])
errored = sorted([c for c,(nf,nr,err) in results.items() if err is not None])
ok = sorted([c for c,(nf,nr,err) in results.items() if err is None and nr>0])
print("\nSUMMARY:")
print("  OK (rows>0):", len(ok))
print("  EMPTY (0 rows, no err):", len(empty), empty)
print("  ERRORED:", len(errored), errored)
json.dump(results, open("dev/validate_results.json","w"))
