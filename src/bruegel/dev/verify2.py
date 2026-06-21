import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import importlib.util
spec = importlib.util.spec_from_file_location("bru", os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "bruegel.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for eid in ["china-economic-database","european-clean-tech-tracker"]:
    try:
        rows = m.PARSERS[eid]([])
        print(f"OK  {eid}: {len(rows)} rows | sample: { {k:str(v)[:26] for k,v in list(rows[0].items())} }")
    except Exception as e:
        import traceback; traceback.print_exc(); print(f"ERR {eid}: {e}")
