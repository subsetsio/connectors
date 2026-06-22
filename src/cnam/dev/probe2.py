import sys; sys.path.insert(0, 'src')
import io, csv
import pyarrow.parquet as pq
from subsets_utils import get
base = 'https://data.ameli.fr/api/explore/v2.1/catalog/datasets'
ds = 'couverture-sas'

# CSV export
url = f'{base}/{ds}/exports/csv'
r = get(url, timeout=(10, 180))
print('CSV', ds, 'status', r.status_code, 'bytes', len(r.content), 'ctype', r.headers.get('content-type'))
text = r.content.decode('utf-8')
reader = csv.reader(io.StringIO(text), delimiter=';')
rows = list(reader)
print('  header:', rows[0])
print('  nrows(incl header):', len(rows))
print('  row1:', rows[1] if len(rows) > 1 else None)

# parquet export
url = f'{base}/{ds}/exports/parquet'
r = get(url, timeout=(10, 180))
print('PARQUET', 'status', r.status_code, 'bytes', len(r.content), 'ctype', r.headers.get('content-type'))
t = pq.read_table(io.BytesIO(r.content))
print('  rows', t.num_rows)
for f in t.schema: print('   ', f.name, f.type)
