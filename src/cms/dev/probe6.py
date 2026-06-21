import duckdb
from subsets_utils import get

# Download a diverse sample of CSVs and test default read_csv_auto (mirrors runtime view).
SAMPLES = [
    ("main",     "https://data.cms.gov/data-api/v1/dataset/01edb62e-5c45-4f43-8c91-16cba21cbb74/data.csv"),
    ("main",     "https://data.cms.gov/data-api/v1/dataset/164fc736-4179-4100-9f79-592b69e41975/data.csv"),  # large
    ("main",     "https://data.cms.gov/data-api/v1/dataset/8889d81e-2ee7-448f-8713-f071038289b5/data.csv"),
    ("provider", "https://data.cms.gov/provider-data/api/1/datastore/query/0127-af37/0/download?format=csv"),
    ("provider", "https://data.cms.gov/provider-data/api/1/datastore/query/footnotes/0/download?format=csv"),
    ("provider", "https://data.cms.gov/provider-data/api/1/datastore/query/hbf-map/0/download?format=csv"),
    ("provider", "https://data.cms.gov/provider-data/api/1/datastore/query/clinical_depression/0/download?format=csv"),
]
import os
os.makedirs("/tmp/cmscsv", exist_ok=True)
for i,(cat,url) in enumerate(SAMPLES):
    path=f"/tmp/cmscsv/s{i}.csv"
    # stream up to 80MB to keep it quick for the large one
    from subsets_utils import get_client
    nbytes=0
    with get_client().stream("GET", url, timeout=60.0) as r, open(path,"wb") as f:
        for chunk in r.iter_bytes(1<<20):
            f.write(chunk); nbytes+=len(chunk)
            if nbytes>80*(1<<20): break
    truncated = nbytes>80*(1<<20)
    try:
        con=duckdb.connect()
        # mirror runtime: read_csv_auto(path)
        res=con.execute(f"SELECT count(*) c FROM read_csv_auto('{path}')").fetchone()
        cols=con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{path}')").fetchall()
        coltypes=[(c[0],c[1]) for c in cols]
        print(f"[{cat}] s{i} OK rows={res[0]} cols={len(cols)} trunc={truncated} bytes={nbytes/1e6:.1f}MB")
        print("    sample coltypes:", coltypes[:6])
    except Exception as e:
        print(f"[{cat}] s{i} FAIL trunc={truncated}: {type(e).__name__}: {str(e)[:200]}")
