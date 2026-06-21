import io, csv
import duckdb, pyarrow as pa
from subsets_utils import get

URL = ("https://data.un.org/_Docs/SYB/CSV/"
       "SYB67_176_202411_Tourist-Visitors%20Arrival%20and%20Expenditure.csv")
text = get(URL, timeout=(10.0,120.0)).text
lines = text.split("\n")
reader = csv.DictReader(io.StringIO("\n".join(lines[1:])))
def pv(r):
    r=(r or "").strip()
    return float(r.replace(",","")) if r else None
rows=[]
for row in reader:
    code=row.get("Region/Country/Area","").strip(); name=row.get("","").strip()
    year=row.get("Year","").strip(); series=row.get("Series","").strip()
    if not code or not year: continue
    s=series.lower()
    if "arrivals" in s: norm,at="arrivals",(row.get("Tourism arrivals series type","").strip() or None)
    elif "expenditure" in s: norm,at="expenditure",None
    else: raise ValueError(series)
    rows.append({"country_code":int(code),"country":name,"year":int(year),
                 "series":norm,"arrivals_type":at,"value":pv(row.get("Value",""))})
t=pa.Table.from_pylist(rows)
con=duckdb.connect(); con.register("raw", t)
res=con.execute('''
  SELECT country_code, max(country) AS country, year,
    max(value) FILTER (WHERE series='arrivals') AS arrivals_thousands,
    max(arrivals_type) FILTER (WHERE series='arrivals') AS arrivals_type,
    max(value) FILTER (WHERE series='expenditure') AS expenditure_millions_usd
  FROM raw GROUP BY country_code, year''').fetch_arrow_table()
print("long rows:", t.num_rows, "wide rows:", res.num_rows)
both=con.execute("""SELECT count(*) FROM (
  SELECT country_code, year,
    max(value) FILTER (WHERE series='arrivals') a,
    max(value) FILTER (WHERE series='expenditure') e
  FROM raw GROUP BY country_code, year) WHERE a IS NOT NULL AND e IS NOT NULL""").fetchone()[0]
print("rows with both arrivals+exp:", both)
print("arrivals null:", res.column("arrivals_thousands").null_count,
      "exp null:", res.column("expenditure_millions_usd").null_count, "of", res.num_rows)
print("distinct arrivals_type:", set(res.column("arrivals_type").to_pylist()))
print("sample:", {k:v[:5] for k,v in res.slice(0,5).to_pydict().items()})
