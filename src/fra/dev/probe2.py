import io, csv
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get, get_client

BASE = "https://data.transportation.gov/resource/{id}.csv"

def header_cols(view):
    r = get(BASE.format(id=view), params={"$limit": 0}, timeout=60.0)
    r.raise_for_status()
    return next(csv.reader([r.text.strip()]))

class StreamReader(io.RawIOBase):
    def __init__(self, it):
        self._it = it; self._buf = b""
    def readable(self): return True
    def readinto(self, b):
        while not self._buf:
            try: self._buf = next(self._it)
            except StopIteration: return 0
        n = min(len(b), len(self._buf))
        b[:n] = self._buf[:n]; self._buf = self._buf[n:]
        return n

def stream_table(view, cols, stop_after=None):
    ct = pacsv.ConvertOptions(column_types={c: pa.string() for c in cols})
    ro = pacsv.ReadOptions(block_size=1<<20)
    url = BASE.format(id=view)
    c = get_client()
    with c.stream("GET", url, params={"$limit": 20000000, "$order": ":id"}, timeout=600.0) as r:
        r.raise_for_status()
        fobj = io.BufferedReader(StreamReader(r.iter_bytes(1<<16)))
        reader = pacsv.open_csv(fobj, read_options=ro, convert_options=ct)
        total = 0; ncols=None
        for batch in reader:
            total += batch.num_rows; ncols = batch.num_columns
            if stop_after and total >= stop_after: 
                return total, ncols, "partial"
        return total, ncols, "complete"

for v in ["m8i6-zdsy"]:
    cols = header_cols(v)
    print(v, "header ncols", len(cols), cols[:5])
    print("  ->", stream_table(v, cols))
# just confirm a 5M table STARTS streaming
v="vhwz-raag"
cols = header_cols(v)
print(v, "header ncols", len(cols), cols[:5])
print("  partial ->", stream_table(v, cols, stop_after=120000))
