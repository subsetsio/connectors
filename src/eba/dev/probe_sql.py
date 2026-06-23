import io, csv as _csv
import duckdb, pyarrow as pa, pyarrow.csv as pacsv
from subsets_utils import get

# small slice of a TE file (first ~400KB) to test the transform SQL shape
url = "https://www.eba.europa.eu/assets/TE2024/Full_database/256109/tr_sov.csv"
content = get(url, headers={"Range":"bytes=0-400000"}, timeout=(10,120)).content
content = content[:content.rfind(b"\n")]  # drop partial last line
header = content.split(b"\n",1)[0].decode("utf-8-sig")
cols = next(_csv.reader([header]))
ct = {c: pa.string() for c in cols}
tbl = pacsv.read_csv(io.BytesIO(content), convert_options=pacsv.ConvertOptions(column_types=ct, strings_can_be_null=True))
con = duckdb.connect()
con.register("eba-te-sovereign-exposures", tbl)
sql = '''
    SELECT * EXCLUDE ("Footnote","Row","Column","Sheet")
        REPLACE (CAST("Period" AS INTEGER) AS "Period", TRY_CAST("Amount" AS DOUBLE) AS "Amount")
    FROM "eba-te-sovereign-exposures"
    WHERE TRY_CAST("Amount" AS DOUBLE) IS NOT NULL
'''
res = con.execute(sql).arrow()
print("TE rows in:", tbl.num_rows, "out:", res.num_rows)
print("TE out cols:", res.column_names)
print("Period dtype:", res.schema.field("Period").type, "Amount:", res.schema.field("Amount").type)

# KRI typed table mock
kri = pa.table({"period":pa.array([201412,202603],pa.int32()),"country":["AT","EU"],
                "indicator_code":["AQT_3.1","FND_32"],"indicator_name":["x","y"],
                "value":pa.array([0.06,None],pa.float64())})
con.register("eba-risk-dashboard-kri", kri)
ksql='SELECT CAST(period AS INTEGER) AS period, country, indicator_code, indicator_name, CAST(value AS DOUBLE) AS value FROM "eba-risk-dashboard-kri" WHERE value IS NOT NULL'
kres=con.execute(ksql).arrow()
print("KRI out rows:", kres.num_rows, "cols:", kres.column_names)
