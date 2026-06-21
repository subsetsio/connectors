import sys, xml.etree.ElementTree as ET
sys.path.insert(0,"src")
import duckdb, pyarrow as pa
from nodes.banco_de_la_rep_blica import _fetch_dataflow, _parse_observations, SCHEMA, _TRANSFORM_SQL
for df in ["DF_TRM_DAILY_HIST","DF_MONAGG_MONTHLY_HIST","DF_DTF_TRIM_ANTICIPADO_HIST","DF_TES_MONTHLY_HIST"]:
    rows=_parse_observations(_fetch_dataflow(df))
    t=pa.Table.from_pylist(rows,schema=SCHEMA)
    con=duckdb.connect(); con.register("d",t)
    sql=_TRANSFORM_SQL.format(dep="d").replace('"d"','d')
    res=con.execute(sql).fetchdf()
    stats=con.execute(f"SELECT min(date),max(date),count(*),count(distinct subject),sum(CASE WHEN date IS NULL THEN 1 ELSE 0 END) FROM ({sql})").fetchall()[0]
    print("="*50, df, "raw",len(t))
    print("  cols:", list(res.columns))
    print("  min/max date, rows, n_subj, null_dates:", stats)
