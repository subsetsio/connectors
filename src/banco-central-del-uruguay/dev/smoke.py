from datetime import date
import pyarrow as pa
import importlib
m = importlib.import_module("nodes.banco_central_del_uruguay")
codes = m._enumerate_currencies(m._GROUP)
print("codes:", len(codes))
rows = m._fetch_window(codes, date(2025,6,2), date(2025,6,20), m._GROUP)
print("rows:", len(rows))
print("sample:", rows[0])
t = pa.Table.from_pylist(rows, schema=m._SCHEMA)
print("table ok:", t.num_rows, "cols", t.column_names)
print("distinct iso:", len(set(r['codigo_iso'] for r in rows)))
# empty window
e = m._fetch_window(codes, date(1990,1,4), date(1990,1,31), m._GROUP)
print("empty window rows:", len(e))
