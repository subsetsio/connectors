import duckdb
url = "https://zenodo.org/api/records/14718294/files/PROJresult_AGE_SSP1_V14.csv/content"
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
print("rows, regions, years, agest range:")
print(con.execute(f"""
  SELECT count(*) n, count(DISTINCT region) nreg, count(DISTINCT Time) nyear,
         min(agest) mina, max(agest) maxa,
         count(DISTINCT sex) nsex, count(DISTINCT edu) nedu
  FROM read_csv_auto('{url}')
""").fetchall())
print("sample distinct edu, sex, agest:")
print(con.execute(f"SELECT DISTINCT edu FROM read_csv_auto('{url}') ORDER BY 1").fetchall())
print("nulls in numeric cols (pop,births,deaths):")
print(con.execute(f"""
  SELECT sum(CASE WHEN pop IS NULL THEN 1 ELSE 0 END) pop_null,
         sum(CASE WHEN deaths IS NULL THEN 1 ELSE 0 END) deaths_null,
         min(pop) minpop, max(pop) maxpop
  FROM read_csv_auto('{url}')
""").fetchall())
print("region sample (incl aggregates?):")
print(con.execute(f"SELECT DISTINCT region FROM read_csv_auto('{url}') ORDER BY region LIMIT 8").fetchall())
print(con.execute(f"SELECT DISTINCT region FROM read_csv_auto('{url}') WHERE region LIKE 'reg9%' ORDER BY region").fetchall())
