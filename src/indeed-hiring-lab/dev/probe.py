import csv, io, duckdb
from subsets_utils import get

def fetch(repo, branch, path):
    r = get(f"https://raw.githubusercontent.com/hiring-lab/{repo}/{branch}/{path}", timeout=(10,120))
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.content.decode("utf-8-sig"))))

con = duckdb.connect()

# wage by country: month 'Jan-19' parse, NA->null
rows = fetch("indeed-wage-tracker","main","posted-wage-growth-by-country.csv")
con.register("w", duckdb.from_arrow.__self__ if False else None) if False else None
import pyarrow as pa
def reg(name, rows):
    con.register(name, pa.Table.from_pylist([{k:(v if v!="" else None) for k,v in r.items()} for r in rows]))
reg("w", rows)
print("WAGE:", con.execute("""
  SELECT jobcountry, CAST(try_strptime(month,'%b-%y') AS DATE) AS m,
         TRY_CAST(posted_wage_growth_yoy AS DOUBLE) AS y,
         TRY_CAST(posted_wage_growth_yoy_3moavg AS DOUBLE) AS y3
  FROM w WHERE try_strptime(month,'%b-%y') IS NOT NULL LIMIT 3
""").fetchall())
print("WAGE rows kept:", con.execute("SELECT count(*) FROM w WHERE try_strptime(month,'%b-%y') IS NOT NULL").fetchone())

# pay transparency country: NA in 3ma
rows = fetch("pay-transparency","main","pay-transparency-country.csv")
reg("p", rows)
print("PAY:", con.execute("""
  SELECT TRY_CAST(date AS DATE) d, country_code,
         TRY_CAST(pay_transparency_pct AS DOUBLE) p,
         TRY_CAST(pay_transparency_pct_3ma AS DOUBLE) p3
  FROM p WHERE TRY_CAST(date AS DATE) IS NOT NULL LIMIT 3
""").fetchall())

# aggregate multi-country union count
rows=[]
for c in ("AU","US","GB"):
    rows += fetch("job_postings_tracker","master",f"{c}/aggregate_job_postings_{c}.csv")
reg("a", rows)
print("AGG countries:", con.execute("SELECT count(distinct jobcountry) FROM a").fetchone(),
      "rows:", con.execute("SELECT count(*) FROM a WHERE TRY_CAST(date AS DATE) IS NOT NULL").fetchone())
