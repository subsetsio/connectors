import sys; sys.path.insert(0,"src")
import duckdb
from nodes import nasdaq as nd
# 1) ETF pagination
etf = nd._etf_rows()
print("etf rows:", len(etf), "(expect ~4526)")
# 2) earnings transform with report_date as real DATE (cloud inference)
con=duckdb.connect()
con.execute("""CREATE TABLE "nasdaq-earnings" AS SELECT * FROM (VALUES
  (DATE '2026-06-18','KR','Kroger','time-pre-market','$37,000,000','Apr/2026','$1.59','8','6/20/2025','$1.49')
) t(report_date,symbol,name,time,marketCap,fiscalQuarterEnding,epsForecast,noOfEsts,lastYearRptDt,lastYearEPS)""")
sql=[s for s in nd.TRANSFORM_SPECS if s.id=="nasdaq-earnings-transform"][0].sql
df=con.execute(sql).fetchdf()
print("earnings transform OK:", df.to_dict('records'))
