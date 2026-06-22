import sys, time, traceback
sys.path.insert(0, ".")
from datasets import energy_crisis, divisia, russian_trade, reer, gini, labour_market, renewables, gas_imports, trade, sovereign, fms
from utils import resolve_links

mods = {
  "energy_crisis": energy_crisis, "divisia": divisia, "russian_trade": russian_trade,
  "reer": reer, "gini": gini, "labour_market": labour_market, "renewables": renewables,
  "gas_imports": gas_imports, "trade": trade, "sovereign": sovereign, "fms": fms,
}
target = sys.argv[1] if len(sys.argv)>1 else None
for name, mod in mods.items():
    if target and name != target: continue
    t0=time.time()
    try:
        links = resolve_links(mod.PAGE_PATH)
        t1=time.time()
        rows = mod.parse(links)
        t2=time.time()
        print(f"OK   {name}: links={t1-t0:.1f}s parse={t2-t1:.1f}s rows={len(rows)} link0={links[0][:90]}")
    except Exception as e:
        print(f"FAIL {name}: {time.time()-t0:.1f}s {type(e).__name__}: {str(e)[:150]}")
