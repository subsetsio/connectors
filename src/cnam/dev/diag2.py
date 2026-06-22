import sys, time; sys.path.insert(0, 'src')
from subsets_utils import get
base = 'https://data.ameli.fr/api/explore/v2.1/catalog/datasets'
ds = 'couverture-sas'
for fmt in ['parquet', 'csv']:
    t0 = time.time()
    try:
        r = get(f'{base}/{ds}/exports/{fmt}', timeout=(8, 60))
        print(f'{fmt}: status {r.status_code} bytes {len(r.content)} in {time.time()-t0:.1f}s ctype={r.headers.get("content-type")}')
    except Exception as e:
        print(f'{fmt}: ERR {type(e).__name__} {str(e)[:150]} after {time.time()-t0:.1f}s')
