import sys, os, re, io, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pyarrow.parquet as pq
from subsets_utils import get

TAGS=json.load(open(os.path.join(os.path.dirname(__file__),"tags.json")))
def _stem(name):
    n=name[:-8] if name.endswith(".parquet") else name
    n=re.sub(r"_?(?:19|20)\d\d","",n); n=re.sub(r"__+","_",n).strip("_"); return n
def assets(tag):
    r=get(f"https://api.github.com/repos/nflverse/nflverse-data/releases/tags/{tag}",
          headers={"Accept":"application/vnd.github+json"},timeout=(10,60)); r.raise_for_status()
    return [a["name"] for a in r.json()["assets"] if a["name"].endswith(".parquet")]
cache={}
out={}
for ent,tag in TAGS.items():
    files=cache.get(tag)
    if files is None: files=cache[tag]=assets(tag)
    m=sorted(f for f in files if _stem(f)==ent)
    pick=m[-1]
    r=get(f"https://github.com/nflverse/nflverse-data/releases/download/{tag}/{pick}",timeout=(10,180)); r.raise_for_status()
    t=pq.read_table(io.BytesIO(r.content))
    cols={f.name:str(f.type) for f in t.schema}
    out[ent]={"file":pick,"nfiles":len(m),"rows_one":t.num_rows,"ncols":len(cols),"cols":cols}
    print(f"\n### {ent}  (tag={tag}, files={len(m)}, pick={pick}, rows={t.num_rows}, ncols={len(cols)})")
    print(", ".join(f"{k}:{v}" for k,v in list(cols.items())[:25]))
json.dump(out, open(os.path.join(os.path.dirname(__file__),"schemas.json"),"w"))
