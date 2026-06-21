import subsets_utils as su
import duckdb, gzip, os, tempfile

ids = ["24w5-nppr", "29hc-w46k", "2den-c3u2"]
tmp = tempfile.mkdtemp()
for did in ids:
    url = f"https://data.cdc.gov/api/views/{did}/rows.csv?accessType=DOWNLOAD"
    client = su.get_client()
    path = os.path.join(tmp, f"{did}.csv.gz")
    with client.stream("GET", url, timeout=(10,300)) as r:
        r.raise_for_status()
        with gzip.open(path, "wb") as f:
            for chunk in r.iter_bytes(1<<20):
                f.write(chunk)
    size = os.path.getsize(path)
    try:
        rel = duckdb.sql(f"SELECT * FROM read_csv_auto('{path}')")
        n = duckdb.sql(f"SELECT count(*) FROM read_csv_auto('{path}')").fetchone()[0]
        cols = rel.columns
        types = [str(t) for t in rel.types]
        print(f"{did}: gz_bytes={size} rows={n} ncols={len(cols)}")
        print("   cols:", list(zip(cols, types))[:6])
    except Exception as e:
        print(f"{did}: DUCKDB ERR {type(e).__name__}: {str(e)[:200]}")
