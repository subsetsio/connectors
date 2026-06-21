import io, csv
import pyarrow as pa
from subsets_utils import get_client
BASE="https://data.transportation.gov/resource/{v}.csv"
class SR(io.RawIOBase):
    def __init__(self, it): self._it=it; self._buf=b""
    def readable(self): return True
    def readinto(self,b):
        while not self._buf:
            try: self._buf=next(self._it)
            except StopIteration: return 0
        n=min(len(b),len(self._buf)); b[:n]=self._buf[:n]; self._buf=self._buf[n:]; return n
def count(view):
    with get_client().stream("GET", BASE.format(v=view), params={"$limit":20000000,"$order":":id"}, timeout=600.0) as r:
        r.raise_for_status()
        text=io.TextIOWrapper(io.BufferedReader(SR(r.iter_bytes(1<<16))), encoding="utf-8", newline="")
        reader=csv.reader(text)
        header=next(reader); ncol=len(header)
        n=0; ragged=0; maxc=ncol; minc=ncol
        for row in reader:
            if len(row)!=ncol: ragged+=1; maxc=max(maxc,len(row)); minc=min(minc,len(row))
            n+=1
        return ncol, n, ragged, minc, maxc
print("85tf-25kj ->", count("85tf-25kj"))  # was failing; expect 224514 rows
