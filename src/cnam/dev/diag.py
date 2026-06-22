import sys; sys.path.insert(0, 'src')
from subsets_utils import get
base = 'https://data.ameli.fr/api/explore/v2.1/catalog/datasets'

# 1. catalog (small, fast) - does basic GET work?
try:
    r = get(base, params={'limit': 1}, timeout=(8, 20))
    print('CATALOG status', r.status_code, 'bytes', len(r.content))
except Exception as e:
    print('CATALOG ERR', type(e).__name__, str(e)[:200])

# 2. records endpoint (json) small
try:
    r = get(f'{base}/couverture-sas/records', params={'limit': 1}, timeout=(8, 20))
    print('RECORDS status', r.status_code, 'bytes', len(r.content), r.text[:150])
except Exception as e:
    print('RECORDS ERR', type(e).__name__, str(e)[:200])

# 3. export json with short read timeout
try:
    r = get(f'{base}/couverture-sas/exports/json', timeout=(8, 30))
    print('EXPORT-JSON status', r.status_code, 'bytes', len(r.content))
except Exception as e:
    print('EXPORT-JSON ERR', type(e).__name__, str(e)[:200])
