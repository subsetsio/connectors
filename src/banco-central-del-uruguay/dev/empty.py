from datetime import date
import importlib
m = importlib.import_module("nodes.banco_central_del_uruguay")
codes = m._enumerate_currencies(m._GROUP)
e = m._fetch_window(codes, date(1990,1,4), date(1990,1,31), m._GROUP)
print("rows:", len(e))
for r in e: print(repr(r))
