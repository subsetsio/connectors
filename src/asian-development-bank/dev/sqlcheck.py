from subsets_utils import get
import io, csv, duckdb, pyarrow as pa

txt = get("https://kidb.adb.org/api/v4/sdmx/data/ADB,PPL_POP/A..?format=sdmx-csv", timeout=(10,180)).text
cols = ["DATAFLOW","FREQ","INDICATOR","ECONOMY_CODE","TIME_PERIOD","OBS_VALUE","UNIT","UNIT_MULT","DECIMALS","OBS_STATUS","REF_YEAR","BASE_YEAR","DATA_SOURCE","METHODOLOGY","FOOTNOTE"]
data={c:[] for c in cols}
for row in csv.DictReader(io.StringIO(txt)):
    for c in cols: data[c].append(row.get(c))
t=pa.table({c:pa.array(data[c],type=pa.string()) for c in cols})
con=duckdb.connect()
con.register("raw", t)
sql='''
SELECT INDICATOR AS indicator, ECONOMY_CODE AS economy_code,
  CAST(TIME_PERIOD AS INTEGER) AS year, CAST(OBS_VALUE AS DOUBLE) AS value,
  NULLIF(UNIT,'') AS unit, TRY_CAST(NULLIF(UNIT_MULT,'') AS INTEGER) AS unit_mult,
  TRY_CAST(NULLIF(DECIMALS,'') AS INTEGER) AS decimals, NULLIF(OBS_STATUS,'') AS obs_status,
  NULLIF(REF_YEAR,'') AS ref_year, NULLIF(BASE_YEAR,'') AS base_year,
  NULLIF(DATA_SOURCE,'') AS data_source, NULLIF(FOOTNOTE,'') AS footnote
FROM raw
WHERE OBS_VALUE IS NOT NULL AND OBS_VALUE <> ''
  AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
  AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
  AND INDICATOR IS NOT NULL AND ECONOMY_CODE IS NOT NULL
'''
r=con.execute(sql).fetchall()
print("rows:", len(r))
print("distinct economies:", con.execute(f"SELECT count(distinct economy_code) FROM ({sql})").fetchone())
print("year range:", con.execute(f"SELECT min(year),max(year) FROM ({sql})").fetchone())
print("dup (indicator,economy,year):", con.execute(f"SELECT count(*) FROM (SELECT indicator,economy_code,year,count(*) c FROM ({sql}) GROUP BY 1,2,3 HAVING c>1)").fetchone())
print(con.execute(f"SELECT * FROM ({sql}) LIMIT 2").fetchdf().to_string())
