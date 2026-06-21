import io, os, csv, zipfile, tempfile
import duckdb, pyarrow as pa
from nodes import fec
CY="2026"
specs={s.id:s for s in fec.TRANSFORM_SPECS}
def sample_view(name,prefix,cols,limit=30000):
    zp=fec._stream_zip_to_tempfile(f"{fec.BULK}/{CY}/{prefix}{CY[2:]}.zip")
    zf=zipfile.ZipFile(zp); m=[n for n in zf.namelist() if not n.startswith('__MACOSX')][0]
    rows=[]
    with zf.open(m) as raw:
        rdr=csv.reader(io.TextIOWrapper(raw,encoding='latin-1',newline=''),delimiter='|',quoting=csv.QUOTE_NONE)
        for f in rdr:
            if len(f)<len(cols): continue
            rows.append(f[:len(cols)])
            if len(rows)>=limit: break
    os.unlink(zp)
    colsT=list(zip(*rows))
    arrays=[pa.array([CY]*len(rows),pa.string())]+[pa.array([v if v!='' else None for v in colsT[i]],pa.string()) for i in range(len(cols))]
    duckdb.sql(f'CREATE OR REPLACE TEMP TABLE "{name}" AS SELECT * FROM tbl_arrow', alias=None) if False else duckdb.register(name, pa.table(arrays,names=["cycle"]+cols))
for name,prefix,cols in [("fec-operating-expenditures","oppexp",fec.OPPEXP_COLS),("fec-inter-committee-transactions","oth",fec.OTH_COLS)]:
    sample_view(name,prefix,cols)
    s=specs[name+"-transform"]
    t=duckdb.sql(s.sql).to_arrow_table()
    # check transaction_date parsed (non-null share)
    nn=duckdb.sql(f'SELECT count(*) total, count(transaction_date) dated, count(amount) amt FROM ({s.sql})').fetchone()
    print(f"[{name}] rows={t.num_rows:,} dated={nn[1]:,} amt={nn[2]:,}")
    assert t.num_rows>0 and nn[1]>0 and nn[2]>0
print("OPPEXP+OTH OK")
