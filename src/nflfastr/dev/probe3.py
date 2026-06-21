import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb
from subsets_utils import get
with tempfile.TemporaryDirectory() as td:
    locs=[]
    for f in ["play_by_play_2024.parquet","play_by_play_2025.parquet"]:
        r=get(f"https://github.com/nflverse/nflverse-data/releases/download/pbp/{f}",timeout=(10,120)); r.raise_for_status()
        p=os.path.join(td,f); open(p,"wb").write(r.content); locs.append(p)
    rel=duckdb.connect().sql(f"SELECT * FROM read_parquet({locs!r}, union_by_name=true)")
    rdr=rel.fetch_record_batch(rows_per_batch=20000)
    sizes=[b.num_rows for b in rdr]
    print("batch sizes:", sizes[:10], "...n=",len(sizes), "total", sum(sizes))
