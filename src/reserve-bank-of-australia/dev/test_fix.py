import sys; sys.path.insert(0,"src")
import duckdb, pyarrow as pa
from nodes.reserve_bank_of_australia import (_fetch_csv_text,_parse_rba_csv,_transform_sql,_RAW_SCHEMA,configure_http,_USER_AGENT)
configure_http(headers={"User-Agent":_USER_AGENT})
for slug in ["a5-data","c9-data","d10-data"]:
    rows=_parse_rba_csv(_fetch_csv_text(slug), slug, None)
    dep=f"reserve-bank-of-australia-{slug}"
    tbl=pa.Table.from_pylist(rows, schema=_RAW_SCHEMA)
    con=duckdb.connect(); con.register(dep,tbl)
    res=con.execute(_transform_sql(dep)).fetch_arrow_table()
    print(f"{slug}: raw={len(tbl)} published={len(res)}")
    if len(res): print("   sample:", {k:res.slice(0,1).to_pylist()[0][k] for k in ('date','series_id','units','value','value_text')})
