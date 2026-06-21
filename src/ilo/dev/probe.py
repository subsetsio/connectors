import sys; sys.path.insert(0,'src')
import csv, io, gzip
import pyarrow as pa, duckdb
from subsets_utils import get
import importlib.util
spec=importlib.util.spec_from_file_location('ilo_nodes','src/nodes/ilo.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def build_table(entity_id):
    raw=m._fetch_csv_gz(entity_id).decode('utf-8-sig')
    r=csv.DictReader(io.StringIO(raw))
    cols={c:[] for c in [f.name for f in m.RAW_SCHEMA]}
    for row in r:
        cols['ref_area'].append(row.get('ref_area')); cols['source'].append(row.get('source'))
        cols['indicator'].append(row.get('indicator')); cols['sex'].append(row.get('sex'))
        cols['classif1'].append(row.get('classif1')); cols['classif2'].append(row.get('classif2'))
        cols['time_period'].append(row.get('time')); cols['obs_value'].append(m._to_float(row.get('obs_value')))
        cols['obs_status'].append(row.get('obs_status'))
    return pa.table({c:pa.array(cols[c], m.RAW_SCHEMA.field(c).type) for c in cols}, schema=m.RAW_SCHEMA)

for eid in ['UNE_TUNE_SEX_AGE_NB_A','UNE_TUNE_SEX_AGE_NB_Q','UNE_TUNE_SEX_AGE_NB_M','CCF_XOXR_CUR_RT_A']:
    did=f"ilo-{eid.lower().replace('_','-')}"
    t=build_table(eid)
    i=[j for j,s in enumerate(m.DOWNLOAD_SPECS) if s.id==did][0]
    sql=m.TRANSFORM_SPECS[i].sql
    con=duckdb.connect()
    con.register(did, t)
    out=con.execute(sql).fetch_arrow_table()
    print(f"\n=== {eid}: raw {t.num_rows} rows -> transform {out.num_rows} rows; cols={out.column_names}")
    print(out.slice(0,3).to_pylist())
    # null date check
    nd=con.execute(f"SELECT count(*) FROM ({sql}) WHERE date IS NULL").fetchone()[0]
    print("null dates:", nd)
