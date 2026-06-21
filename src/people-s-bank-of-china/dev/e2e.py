import sys, duckdb
sys.path.insert(0,"src")
from nodes.people_s_bank_of_china import fetch_one, _BY_SPEC, _transform_sql
from subsets_utils import load_raw_ndjson
sid="people-s-bank-of-china-money-and-banking-statistics--money-supply"
print("category/title:",_BY_SPEC[sid])
fetch_one(sid)
rows=load_raw_ndjson(sid)
print("raw rows:",len(rows))
print("sample:",rows[0])
print("years:",sorted({r['source_year'] for r in rows}))
print("periods:",len(set(r['period'] for r in rows)),"items:",sorted(set(r['item'] for r in rows)))
# run transform
con=duckdb.connect()
con.register("t", __import__("pyarrow").Table.from_pylist(rows))
con.execute(f'CREATE VIEW "{sid}" AS SELECT * FROM t')
res=con.execute(_transform_sql(sid)).fetch_arrow_table()
print("\nTRANSFORM rows:",res.num_rows,"cols:",res.column_names)
print(res.slice(0,5).to_pylist())
print("...tail:",res.slice(res.num_rows-3,3).to_pylist())
