import io, duckdb, openpyxl, pyarrow as pa
import sys; sys.path.insert(0, "src")
from nodes.macrohistory_database import _COLUMNS, _arrow_type, SCHEMA, TRANSFORM_SPECS, DATASET_URL
from subsets_utils import get
content = get(DATASET_URL, timeout=(10,120)).content
ws = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True).worksheets[0]
it = ws.iter_rows(values_only=True); next(it)
cols={c:[] for c in _COLUMNS}
for row in it:
    if all(v is None for v in row): continue
    for c,v in zip(_COLUMNS,row): cols[c].append(v)
tbl = pa.Table.from_arrays([pa.array(cols[c],type=_arrow_type(c)) for c in _COLUMNS], schema=SCHEMA)
print("raw rows", tbl.num_rows)
con = duckdb.connect()
con.register("macrohistory-database-jst-macrohistory-panel", tbl)
sql = TRANSFORM_SPECS[0].sql
res = con.execute(sql).fetch_arrow_table()
print("transform rows", res.num_rows, "cols", res.num_columns)
print("countries", len(set(res.column('country').to_pylist())))
yrs=[y for y in res.column('year').to_pylist() if y is not None]
print("year range", min(yrs), max(yrs))
print("sample cols", res.column_names[:6], "...", res.column_names[-4:])
