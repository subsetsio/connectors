import nodes.itu as m
import subsets_utils as su

m.fetch_countries("itu-countries")
m.fetch_indicators("itu-indicators")
c = su.load_raw_parquet("itu-countries")
i = su.load_raw_parquet("itu-indicators")
print("countries rows:", c.num_rows, "cols:", c.column_names)
print("indicators rows:", i.num_rows, "cols:", i.column_names)

# values: run a 2-indicator slice manually to validate the streaming path
code_ids, _ = m._catalogue_code_ids()
cids = m._country_ids()
import pyarrow.parquet as pq
total = 0
with su.raw_parquet_writer("itu-values-smoke", m._VALUES_SCHEMA) as w:
    for cid in code_ids[:3]:
        rows = m._download_indicator_csv(cid, cids)
        print("  code", cid, "->", (len(rows) if rows else 0), "rows")
        if rows:
            t = m._values_table(cid, rows); w.write_table(t); total += t.num_rows
v = su.load_raw_parquet("itu-values-smoke")
print("values-smoke rows:", v.num_rows, "cols:", v.column_names)
print("sample:", {k: v.column(k)[0].as_py() for k in v.column_names})
