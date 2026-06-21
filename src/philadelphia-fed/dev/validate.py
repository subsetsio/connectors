"""Exercise every fetch fn's parse path WITHOUT writing to the raw layer.
Monkeypatches save_raw_parquet to capture + summarize the table instead."""
import sys
import pyarrow as pa
import subsets_utils

captured = {}


def fake_save(table, asset_id):
    captured[asset_id] = table
    return f"(captured {asset_id})"


subsets_utils.save_raw_parquet = fake_save
import nodes.philadelphia_fed as m
m.save_raw_parquet = fake_save

only = sys.argv[1] if len(sys.argv) > 1 else None
for spec in m.DOWNLOAD_SPECS:
    eid = spec.id.replace("philadelphia-fed-", "")
    if only and only not in spec.id:
        continue
    try:
        spec.fn(spec.id)
        t = captured[spec.id]
        print(f"OK  {spec.id:60s} rows={len(t):>7,} cols={t.column_names}")
        # show a couple of sample values for sanity
        print("      sample:", {c: t.column(c)[0].as_py() for c in t.column_names})
    except Exception as e:
        import traceback
        print(f"FAIL {spec.id}: {type(e).__name__}: {e}")
        traceback.print_exc()
