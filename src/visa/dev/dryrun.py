import sys; sys.path.insert(0,"src")
import nodes.visa as v
import pyarrow as pa

# monkeypatch save to capture instead of writing to prod raw
captured={}
def fake_save(table, asset): captured[asset]=table
v.save_raw_parquet=fake_save

v.fetch_north_america("visa-north-america-smi")
v.fetch_global("visa-global-smi")
for k,t in captured.items():
    print(k, "rows=",len(t), "cols=",t.column_names)
    print("  date range:", pa.compute.min(t["date"]).as_py(), "..", pa.compute.max(t["date"]).as_py())
    print("  index min/max:", pa.compute.min(t["index_value"]).as_py(), pa.compute.max(t["index_value"]).as_py())
na=captured["visa-north-america-smi"]
print("NA geos:", set(na["geography"].to_pylist()))
print("NA segs:", set(na["spending_segment"].to_pylist()))
print("NA adj:", set(na["seasonal_adjustment"].to_pylist()))
gl=captured["visa-global-smi"]
print("GL codes:", set(gl["country_code"].to_pylist()))
print("GL segs:", set(gl["spending_segment"].to_pylist()))
