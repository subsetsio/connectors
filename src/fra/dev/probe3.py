import io, csv, sys
import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import get, get_client
BASE = "https://data.transportation.gov/resource/{id}.csv"
def header_cols(view):
    r = get(BASE.format(id=view), params={"$limit": 0}, timeout=60.0); r.raise_for_status()
    return next(csv.reader([r.text.strip()]))
class SR(io.RawIOBase):
    def __init__(self, it): self._it=it; self._buf=b""
    def readable(self): return True
    def readinto(self,b):
        while not self._buf:
            try: self._buf=next(self._it)
            except StopIteration: return 0
        n=min(len(b),len(self._buf)); b[:n]=self._buf[:n]; self._buf=self._buf[n:]; return n
def stream(view, cols, stop=None):
    ct=pacsv.ConvertOptions(column_types={c: pa.string() for c in cols})
    ro=pacsv.ReadOptions(block_size=1<<20)
    with get_client().stream("GET", BASE.format(id=view), params={"$limit":20000000,"$order":":id"}, timeout=600.0) as r:
        r.raise_for_status()
        rd=pacsv.open_csv(io.BufferedReader(SR(r.iter_bytes(1<<16))), read_options=ro, convert_options=ct)
        tot=0; nc=None
        for b in rd:
            tot+=b.num_rows; nc=b.num_columns
            if stop and tot>=stop: return tot,nc,"partial"
        return tot,nc,"complete"
v="m8i6-zdsy"; cols=header_cols(v)
print(v,"hdr",len(cols),cols[:4]); sys.stdout.flush()
print("  full ->", stream(v,cols)); sys.stdout.flush()
