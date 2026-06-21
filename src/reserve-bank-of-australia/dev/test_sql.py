import sys; sys.path.insert(0,"src")
import duckdb, pyarrow as pa
from nodes.reserve_bank_of_australia import (_fetch_csv_text,_parse_rba_csv,_transform_sql,_RAW_SCHEMA,configure_http,_USER_AGENT)
configure_http(headers={"User-Agent":_USER_AGENT})

cases = {
  "reserve-bank-of-australia-g1-data": [("g1-data",None)],
  "reserve-bank-of-australia-a2-data": [("a2-data",None)],
  "reserve-bank-of-australia-j1-forecasts": [("j1-cash-rate","cash-rate"),("j1-gdp-growth","gdp-growth")],
}
for dep, members in cases.items():
    rows=[]
    for slug,pk in members:
        rows += _parse_rba_csv(_fetch_csv_text(slug), slug, pk)
    tbl=pa.Table.from_pylist(rows, schema=_RAW_SCHEMA)
    con=duckdb.connect()
    con.register(dep, tbl)
    res=con.execute(_transform_sql(dep)).fetch_arrow_table()
    print(f"{dep}: raw={len(tbl)} -> published={len(res)} cols={res.column_names}")
    print("   sample:", res.slice(0,1).to_pylist())
    # numeric coverage
    import pyarrow.compute as pc
    nn = len(res.column("value").drop_null())
    print(f"   numeric value non-null: {nn}/{len(res)}")
