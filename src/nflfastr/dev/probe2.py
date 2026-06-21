import sys, os, re, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb
from subsets_utils import get

def _stem(name):
    n=name[:-len(".parquet")] if name.endswith(".parquet") else name
    n=re.sub(r"_?(?:19|20)\d\d","",n)
    n=re.sub(r"__+","_",n).strip("_")
    return n

def assets(tag):
    url=f"https://api.github.com/repos/nflverse/nflverse-data/releases/tags/{tag}"
    r=get(url, headers={"Accept":"application/vnd.github+json"}, timeout=(10,60)); r.raise_for_status()
    return [a["name"] for a in r.json()["assets"] if a["name"].endswith(".parquet")]

# stem filtering: stats_player tag, want only stats_player_reg (not regpost)
sp=assets("stats_player")
match=[f for f in sp if _stem(f)=="stats_player_reg"]
print("stats_player_reg files:", len(match), match[:3])
print("stats_player_regpost files:", len([f for f in sp if _stem(f)=="stats_player_regpost"]))

# union_by_name streaming on 2 pbp seasons
files=["play_by_play_1999.parquet","play_by_play_2025.parquet"]
with tempfile.TemporaryDirectory() as td:
    locs=[]
    for f in files:
        r=get(f"https://github.com/nflverse/nflverse-data/releases/download/pbp/{f}",timeout=(10,120)); r.raise_for_status()
        p=os.path.join(td,f); open(p,"wb").write(r.content); locs.append(p)
    con=duckdb.connect()
    rel=con.sql(f"SELECT * FROM read_parquet({locs!r}, union_by_name=true)")
    rdr=rel.fetch_record_batch()
    nrows=0; nb=0
    sch=rdr.schema
    for b in rdr:
        nrows+=b.num_rows; nb+=1
    print(f"union pbp 1999+2025: rows={nrows} batches={nb} cols={len(sch)}")
    print("goal_to_go type:", sch.field("goal_to_go").type)
