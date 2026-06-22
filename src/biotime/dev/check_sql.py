import io, csv, zipfile, re
import duckdb, pyarrow as pa
from subsets_utils import get
import nodes.biotime as M

# Build small studies + records arrow tables exactly like the fetch fns do.
meta = get(META_CSV_URL := M.META_CSV_URL, timeout=(10, 120)).content.decode("utf-8", "replace")
mr = csv.reader(io.StringIO(meta)); mh = [h.strip().lower() for h in next(mr)]
mrows = [r for _, r in zip(range(50), mr)]
studies = pa.table({mh[i]: pa.array([(r+[None]*len(mh))[i] for r in mrows], pa.string()) for i in range(len(mh))})

z = get(M.QUERY_ZIP_URL, timeout=(10, 300)).content
zf = zipfile.ZipFile(io.BytesIO(z)); rd = csv.reader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8", errors="replace"))
next(rd)
rrows = [r for _, r in zip(range(2000), rd)]
records = M._batch_to_table(rrows)

con = duckdb.connect()
con.register("biotime-studies", studies)
con.register("biotime-records", records)
for spec in M.TRANSFORM_SPECS:
    sql = re.sub(r'FROM "([^"]+)"', lambda m: f'FROM "{m.group(1)}"', spec.sql)
    out = con.execute(spec.sql).arrow()
    print(spec.id, "->", out.num_rows, "rows,", out.num_columns, "cols:", out.column_names)
