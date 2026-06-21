import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb
for sid in ["pordata-portugal-10","pordata-portugal-130","pordata-portugal-550"]:
    f = sorted(glob.glob(f"data/dev/raw/{sid}.ndjson*"))[0]
    q = f'''SELECT CAST(indicator_id AS INTEGER) AS indicator_id, period,
            TRY_CAST(period AS INTEGER) AS "year", series, series_group,
            CAST(value AS DOUBLE) AS value
            FROM read_ndjson_auto('{f}') WHERE value IS NOT NULL AND series IS NOT NULL'''
    res = duckdb.connect().execute(q).fetchall()
    print(f"{sid}: transform_rows={len(res)} first={res[0]}")
