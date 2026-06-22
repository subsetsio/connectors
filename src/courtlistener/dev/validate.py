import io, csv, sys
import pyarrow as pa
import duckdb
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
from subsets_utils import get_client
import importlib.util
spec = importlib.util.spec_from_file_location("cl", "src/nodes/courtlistener.py")
cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)

def stream_table_to_arrow(table, date="2026-03-31", limit_batches=None):
    url = f"{cl.BASE}{table}-{date}.csv.bz2"
    client = get_client()
    with client.stream("GET", url, timeout=(10,300)) as resp:
        resp.raise_for_status()
        reader = io.BufferedReader(cl._Bz2Reader(resp.iter_bytes(1<<20)), buffer_size=1<<20)
        text = io.TextIOWrapper(reader, encoding="utf-8", errors="replace", newline="")
        rdr = csv.reader(text)
        header = next(rdr)
        ncol = len(header)
        schema = pa.schema([(c, pa.string()) for c in header])
        cols = [[] for _ in range(ncol)]
        batches=[]
        for row in rdr:
            if len(row)!=ncol: row=(row+[None]*ncol)[:ncol]
            for i in range(ncol): cols[i].append(row[i] if row[i]!="" else None)
            if len(cols[0])>=cl.BATCH_ROWS:
                batches.append(pa.record_batch([pa.array(c,pa.string()) for c in cols],schema=schema)); cols=[[] for _ in range(ncol)]
                if limit_batches and len(batches)>=limit_batches: break
        if cols[0]:
            batches.append(pa.record_batch([pa.array(c,pa.string()) for c in cols],schema=schema))
    return pa.Table.from_batches(batches, schema=schema)

for t in ["courts","people-db-political-affiliations","citations"]:
    tbl = stream_table_to_arrow(t)
    print(f"== {t}: {tbl.num_rows} rows, {tbl.num_columns} cols ==")
    con = duckdb.connect()
    con.register(f"courtlistener-{t}", tbl)
    sql = cl._build_sql(t, f"courtlistener-{t}")
    res = con.execute(sql).arrow().read_all() if hasattr(con.execute(sql).arrow(),"read_all") else con.execute(sql).arrow()
    print("  transform ->", res.num_rows, "rows; dtypes:", {f.name:str(f.type) for f in res.schema}.__str__()[:300])
