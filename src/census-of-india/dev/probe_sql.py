import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb
import subsets_utils as su
from utils import install_ca, excel_to_long
install_ca()
url="https://censusindia.gov.in/nada/index.php/catalog/20028/download/23160/PC01_A01.xls"
rows=excel_to_long(su.get(url,timeout=(10,120)).content,"PC01_A01.xls")
for r in rows: r.update(census_year=2001, table_code="A-01", source_file="PC01_A01.xls")
p="dev/_t.ndjson"
open(p,"w").write("\n".join(json.dumps(r) for r in rows))
con=duckdb.connect()
con.execute(f"CREATE VIEW \"asset\" AS SELECT * FROM read_json_auto('{p}')")
sql='''SELECT CAST(census_year AS INTEGER) AS census_year, table_code, source_file, region, dimensions, measure, CAST(value AS DOUBLE) AS value FROM "asset" WHERE value IS NOT NULL'''
out=con.execute(sql).fetch_arrow_table()
print("rows:",out.num_rows)
print("schema:",out.schema)
print(con.execute(sql+" LIMIT 2").fetchall())
os.remove(p)
