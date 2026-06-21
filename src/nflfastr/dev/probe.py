import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, sys
import pyarrow.parquet as pq
from subsets_utils import get

def dl(tag, fn):
    url=f"https://github.com/nflverse/nflverse-data/releases/download/{tag}/{fn}"
    r=get(url, timeout=(10,120)); r.raise_for_status()
    return r.content

# pbp schema drift 1999 vs 2025 + sizes
for yr in (1999,2025):
    b=dl("pbp",f"play_by_play_{yr}.parquet")
    t=pq.read_table(io.BytesIO(b))
    print(f"pbp {yr}: bytes={len(b)} rows={t.num_rows} cols={t.num_columns}")
schemas={}
for yr in (1999,2025):
    b=dl("pbp",f"play_by_play_{yr}.parquet")
    s=pq.read_schema(io.BytesIO(b))
    schemas[yr]={f.name:str(f.type) for f in s}
only99=set(schemas[1999])-set(schemas[2025])
only25=set(schemas[2025])-set(schemas[1999])
common=set(schemas[1999])&set(schemas[2025])
typdiff={c:(schemas[1999][c],schemas[2025][c]) for c in common if schemas[1999][c]!=schemas[2025][c]}
print("cols only in 1999:",len(only99), list(only99)[:10])
print("cols only in 2025:",len(only25), list(only25)[:10])
print("type diffs:",len(typdiff:=typdiff), dict(list(typdiff.items())[:10]))
