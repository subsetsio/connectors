import io, re, tempfile
import pandas as pd, pyarrow as pa, duckdb
from deltalake import write_deltalake
from subsets_utils import get

RAW="https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive"
def read_csv(content, **kw):
    last=None
    for enc in ("utf-8-sig","cp1252","latin-1"):
        try: return pd.read_csv(io.BytesIO(content),dtype=str,encoding=enc,**kw), enc
        except UnicodeDecodeError as e: last=e
    raise last
def safe(cols):
    used=set(); out=[]
    for raw in cols:
        s=re.sub(r"[^0-9A-Za-z]+","_",str(raw)).strip("_") or "col"
        if s[0].isdigit(): s="c_"+s
        b,i=s,2
        while s in used: s=f"{b}_{i}"; i+=1
        used.add(s); out.append(s)
    return out

for year in ("2011","2014","2016","2025"):
    c=get(f"{RAW}/{year}/results.csv",timeout=(10.0,300.0)); c.raise_for_status()
    df,enc=read_csv(c.content,low_memory=False)
    df.columns=safe(df.columns)
    schema=pa.schema([(x,pa.string()) for x in df.columns])
    t=pa.Table.from_pandas(df,schema=schema,preserve_index=False)
    out=duckdb.sql('SELECT * FROM t').arrow()
    d=tempfile.mkdtemp(); write_deltalake(d,out,mode="overwrite")
    print(f"{year} OK enc={enc} rows={t.num_rows} cols={t.num_columns} first={df.columns[0][:30]} last={df.columns[-1][:30]}")
