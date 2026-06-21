import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import importlib.util
spec = importlib.util.spec_from_file_location("bru", os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "bruegel.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
tests = ["divisia-monetary-aggregates-euro-area","sovereign-bond-holdings","russian-foreign-trade-tracker","eu-labour-market-outlook-dashboard","european-natural-gas-demand-tracker"]
for eid in tests:
    try:
        links = m._resolve_links(m.PAGE_PATHS[eid]) if eid in m.PAGE_PATHS else []
        rows = m.PARSERS[eid](links)
        print(f"OK  {eid}: {len(rows)} rows | sample: { {k:str(v)[:22] for k,v in list(rows[0].items())} }")
    except Exception as e:
        import traceback; traceback.print_exc(); print(f"ERR {eid}: {e}")
