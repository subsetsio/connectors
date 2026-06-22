import io, pyarrow.csv as pacsv
from subsets_utils import get

URL = "https://www.cato.org/sites/cato.org/files/human-freedom-index-files/2025-human-freedom-index-data.csv"
resp = get(URL, timeout=(10, 120))
resp.raise_for_status()
data = resp.content
print("bytes:", len(data))
tbl = pacsv.read_csv(io.BytesIO(data))
print("rows:", tbl.num_rows, "cols:", tbl.num_columns)
names = tbl.column_names
print("first 12 cols:", names[:12])
print("last 6 cols:", names[-6:])
# show types of key cols
import pyarrow as pa
sch = tbl.schema
for c in ["year","iso","countries","region","hf_score","hf_rank","hf_quartile","pf_score","ef_score"]:
    if c in names:
        print(f"  {c}: {sch.field(c).type}")
    else:
        print(f"  {c}: MISSING")
# null check on key cols
import pyarrow.compute as pc
for c in ["year","iso","countries"]:
    col = tbl.column(c)
    print(f"nulls in {c}:", pc.sum(pc.is_null(col)).as_py())
# uniqueness of (iso, year)
yrs = tbl.column("year").to_pylist()
isos = tbl.column("iso").to_pylist()
pairs = list(zip(isos, yrs))
print("rows:", len(pairs), "distinct (iso,year):", len(set(pairs)))
print("distinct iso:", len(set(isos)), "year range:", min(yrs), max(yrs))
# how many columns are numeric vs string
from collections import Counter
tc = Counter(str(sch.field(n).type) for n in names)
print("type histogram:", dict(tc))
