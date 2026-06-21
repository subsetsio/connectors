"""Local check of the CSV->parquet helper: nullstr list, whole-file sniff,
multi-file union. No network."""
import sys
sys.path.insert(0, "/Users/nathansnellaert/Documents/hardened/connectors/src/fbi/src")

from nodes.fbi import _csvs_to_parquet  # noqa: E402

# (1) Numeric column whose "NULL" string appears only AFTER a large numeric run,
# mimicking hc.total_individual_victims beyond the 20480 sample.
rows = ["year,agency,total_individual_victims"]
for i in range(30000):
    rows.append(f"2011,AG{i},1")
rows.append("2012,AGX,NULL")          # the value that broke read_csv_auto
csv1 = ("\n".join(rows) + "\n").encode()

t = _csvs_to_parquet([csv1])
print("single-file:", t.num_rows, "rows", t.schema.field("total_individual_victims").type)
assert t.num_rows == 30001
# "NULL" token -> null, so the column should sniff numeric (not VARCHAR).
import pyarrow as pa  # noqa: E402
assert pa.types.is_integer(t.schema.field("total_individual_victims").type), t.schema

# (2) union of two year-range CSVs sharing a schema (assignment-activity case).
a = b"year,ori,count\n1995,A1,5\n1996,A2,6\n"
b = b"year,ori,count\n2020,B1,7\n2021,B2,8\n"
u = _csvs_to_parquet([a, b])
print("union:", u.num_rows, "rows", u.column_names)
assert u.num_rows == 4 and set(u.column_names) == {"year", "ori", "count"}

print("OK")
