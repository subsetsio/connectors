import io, csv, sys
import pyarrow as pa
import duckdb
sys.path.insert(0, "src"); sys.path.insert(0,"src/nodes")
from subsets_utils import get_client
import importlib.util
spec = importlib.util.spec_from_file_location("cl", "src/nodes/courtlistener.py")
cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
def stream(table, date="2026-03-31"):
    url = f"{cl.BASE}{table}-{date}.csv.bz2"; client=get_client()
    with client.stream("GET",url,timeout=(10,300)) as resp:
        resp.raise_for_status()
        reader=io.BufferedReader(cl._Bz2Reader(resp.iter_bytes(1<<20)),buffer_size=1<<20)
        text=io.TextIOWrapper(reader,encoding="utf-8",errors="replace",newline="")
        rdr=csv.reader(text); header=next(rdr); ncol=len(header)
        schema=pa.schema([(c,pa.string()) for c in header]); cols=[[] for _ in range(ncol)]; batches=[]
        for row in rdr:
            if len(row)!=ncol: row=(row+[None]*ncol)[:ncol]
            for i in range(ncol): cols[i].append(row[i] if row[i]!="" else None)
        if cols[0]: batches.append(pa.record_batch([pa.array(c,pa.string()) for c in cols],schema=schema))
    return pa.Table.from_batches(batches,schema=schema)
for t in ["courts","people-db-political-affiliations","citations"]:
    tbl=stream(t); con=duckdb.connect(); con.register(f"courtlistener-{t}",tbl)
    res=con.execute(cl._build_sql(t,f"courtlistener-{t}")).fetch_arrow_table()
    print(f"== {t}: raw {tbl.num_rows}r -> transform {res.num_rows}r ==")
    print("   types:", {f.name:str(f.type) for f in res.schema})
