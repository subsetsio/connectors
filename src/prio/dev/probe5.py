import re, io, zipfile, urllib.parse, tempfile, os
from subsets_utils import get
import pandas as pd, pyarrow.parquet as pq
def links(html):
    seen=set(); res=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        u,f=m.group(1),urllib.parse.unquote(m.group(2))
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res
def dl(u,f): return get(f"https://cdn.cloud.prio.org/files/{u}/{urllib.parse.quote(f)}", timeout=(15,180)).content
def find(i,sub,ext):
    ls=links(get(f"https://www.prio.org/data/{i}",timeout=(10,60)).text)
    for u,f in ls:
        if sub.lower() in f.lower() and f.lower().endswith("."+ext): return u,f
# entity 34 header inspection
u,f=find("34","PFOs Mapping Dataset","xlsx")
raw=dl(u,f)
df0=pd.read_excel(io.BytesIO(raw), engine="openpyxl", header=None, nrows=8)
print("=== /data/34 first 8 rows (header=None) ===")
for r in range(min(8,len(df0))):
    vals=[str(x)[:14] for x in list(df0.iloc[r])[:8]]
    print(f"row{r}:", vals)
# try header=1,2
for h in (1,2,3):
    d=pd.read_excel(io.BytesIO(raw), engine="openpyxl", header=h)
    nonun=[c for c in d.columns if not str(c).startswith("Unnamed")]
    print(f"header={h}: cols={len(d.columns)} named={len(nonun)} sample={[str(c)[:16] for c in list(d.columns)[:6]]}")

# entity 40 pg_static
ls=links(get("https://www.prio.org/data/40",timeout=(10,60)).text)
u,f=[(u,f) for u,f in ls if "3_0_1" in f.lower() and f.endswith(".zip")][0]
zf=zipfile.ZipFile(io.BytesIO(dl(u,f)))
for m in zf.namelist():
    if m.endswith("pg_static.parquet"):
        with tempfile.NamedTemporaryFile(suffix=".parquet",delete=False) as tf: tf.write(zf.read(m)); p=tf.name
        pf=pq.ParquetFile(p)
        print(f"\n=== pg_static.parquet rows={pf.metadata.num_rows} cols={pf.metadata.num_columns} ===")
        print("cols:", [c for c in pf.schema.names][:30])
        os.unlink(p)
