import re, io, zipfile, urllib.parse, tempfile, os
from subsets_utils import get
import pandas as pd, pyarrow as pa, pyarrow.parquet as pq

# (file_substr, file_ext, member_substr_or_None) ; member matched by basename exact-or-contains
CONFIG = {
 "1":  ("Battle Deaths Dataset", "xls", None),
 "3":  ("Annual Onset", "dta", None),
 "4":  ("Armed Conflict Dataset", "zip", "Main Conflict Table.xls"),
 "5":  ("ConflictSite", "xls", None),
 "6":  ("USD 20 Data", "zip", "events.xlsx"),
 "7":  ("ACLED", "zip", "AcledEvents.xls"),
 "8":  ("GEO-SVAC", "zip", "geosvac.csv"),
 "10": ("DIADATA Data", "zip", "DIADATA Excel file.xls"),
 "11": ("PETRODATA v12 Data", "zip", "Petrodata_Onshore_V1.2.xlsx"),
 "16": ("Witches Brew Dataset", "sav", None),
 "20": ("polyarchy v2 data", "zip", "polyarchy v2 dataset.csv"),
 "23": ("Natresconfl", "dta", None),
 "31": ("ConflictRecurrenceDatabase", "csv", None),
 "32": ("USD 30 Dataset", "zip", "events.xlsx"),
 "34": ("PFOs Mapping Dataset", "xlsx", None),
 "35": ("Area Database Data", "csv", None),
 "36": ("SHDI-SGDI-Total", "csv", None),
 "37": ("GDL-CorruptionData", "csv", None),
 "39": ("OMG_Stata", "zip", "omg.dta"),
 "40": ("3_0_1", "zip", "pg_timevarying.parquet"),
}
def links(html):
    seen=set(); res=[]
    for m in re.finditer(r'cdn\.cloud\.prio\.org/files/([0-9a-f-]+)/([^"?\\]+)', html):
        u,f=m.group(1),urllib.parse.unquote(m.group(2))
        if (u,f) in seen: continue
        seen.add((u,f)); res.append((u,f))
    return res
def dl(u,f): return get(f"https://cdn.cloud.prio.org/files/{u}/{urllib.parse.quote(f)}", timeout=(15,300)).content
def parse_df(data, ext, name):
    bio=io.BytesIO(data)
    if ext=="csv":
        for enc in ("utf-8","latin-1"):
            try:
                df=pd.read_csv(io.BytesIO(data), encoding=enc, low_memory=False)
                if df.shape[1]==1:
                    df=pd.read_csv(io.BytesIO(data), encoding=enc, sep=";", low_memory=False)
                return df
            except Exception: continue
        raise RuntimeError("csv parse failed")
    if ext=="xlsx": return pd.read_excel(bio, engine="openpyxl")
    if ext=="xls":  return pd.read_excel(bio, engine="xlrd")
    if ext=="dta":  return pd.read_stata(bio, convert_categoricals=False)
    if ext=="sav":
        import pyreadstat
        with tempfile.NamedTemporaryFile(suffix=".sav", delete=False) as tf:
            tf.write(data); p=tf.name
        try: df,_=pyreadstat.read_sav(p)
        finally: os.unlink(p)
        return df
    raise RuntimeError("ext "+ext)

for i,(fs,fe,mem) in CONFIG.items():
    try:
        ls=links(get(f"https://www.prio.org/data/{i}", timeout=(10,60)).text)
        cand=[(u,f) for u,f in ls if fs.lower() in f.lower() and f.lower().endswith("."+fe)]
        if not cand: print(f"/data/{i}: NO LINK match {fs}.{fe}"); continue
        u,f=cand[0]; data=dl(u,f)
        if fe=="zip":
            zf=zipfile.ZipFile(io.BytesIO(data))
            ms=[m for m in zf.namelist() if not m.split('/')[-1].startswith('._') and '__MACOSX' not in m and not m.endswith('/')]
            pick=[m for m in ms if m.split('/')[-1]==mem] or [m for m in ms if mem.lower() in m.lower()]
            mname=pick[0]; mext=mname.rsplit(".",1)[-1].lower()
            mdata=zf.read(mname)
            if mext=="parquet":
                with tempfile.NamedTemporaryFile(suffix=".parquet",delete=False) as tf: tf.write(mdata); p=tf.name
                pf=pq.ParquetFile(p); print(f"/data/{i}: {f} :: {mname} -> parquet rows={pf.metadata.num_rows} cols={pf.metadata.num_columns}"); os.unlink(p); continue
            df=parse_df(mdata, mext, mname)
        else:
            df=parse_df(data, fe, f)
        print(f"/data/{i}: {f} -> rows={len(df)} cols={len(df.columns)} | {list(df.columns)[:6]}")
    except Exception as e:
        print(f"/data/{i}: ERR {type(e).__name__}: {e}")
