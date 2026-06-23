import sys
sys.path.insert(0, "src")
import nodes.cliwoc as m
import pyarrow as pa

text = m._download_tsv()
import csv, io, datetime as dt
reader = csv.reader(io.StringIO(text), delimiter="\t")
header = next(reader)
idx = {n: i for i, n in enumerate(header)}

def cell(row, name):
    i = idx.get(name)
    if i is None or i >= len(row):
        return ""
    return row[i]

cols = {n: [] for n in m.SCHEMA.names}
for row in reader:
    year = m._to_int(cell(row, "Year")); month = m._to_int(cell(row, "Month")); day = m._to_int(cell(row, "Day"))
    rd = None
    if year and month and day and 1 <= month <= 12 and 1 <= day <= 31 and 1600 <= year <= 1900:
        try: rd = dt.date(year, month, day)
        except ValueError: rd = None
    cols["record_date"].append(rd); cols["year"].append(year); cols["month"].append(month); cols["day"].append(day)
    cols["latitude"].append(m._to_float(cell(row, "latitude"))); cols["longitude"].append(m._to_float(cell(row, "longitude")))
    for pub, src in m.SOURCE_COLS.items():
        cols[pub].append(m._clean(cell(row, src)))

t = pa.table(cols, schema=m.SCHEMA)
print("rows:", t.num_rows, "cols:", t.num_columns)
print("year range:", pa.compute.min(t["year"]).as_py(), pa.compute.max(t["year"]).as_py())
print("lat range:", pa.compute.min(t["latitude"]).as_py(), pa.compute.max(t["latitude"]).as_py())
print("lon range:", pa.compute.min(t["longitude"]).as_py(), pa.compute.max(t["longitude"]).as_py())
print("logbook_id nulls:", t["logbook_id"].null_count)
print("lat nulls:", t["latitude"].null_count)
print("record_date nulls:", t["record_date"].null_count)
import pyarrow.compute as pc
print("distinct nationality:", len(pc.unique(t["nationality"])))
print("sample nationalities:", pc.unique(t["nationality"]).to_pylist()[:15])
