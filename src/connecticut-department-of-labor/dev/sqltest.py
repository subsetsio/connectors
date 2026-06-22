import duckdb
con = duckdb.connect()
# wide monthly unpivot (CES NSA)
con.execute("""
create table ces as select * from (values
  ('1990','09','00000','Total Nonfarm','00000000','01','AE','1629.9','1621.4','1633.1')
) t(year,st,area,industry_title,series,data_type_code,data_type,jan,feb,mar)
""")
print("CES unpivot:")
print(con.execute("""
SELECT CAST(year AS INTEGER) AS year, area, month_name,
       TRY_CAST(val AS DOUBLE) AS value
FROM (UNPIVOT ces ON jan, feb, mar INTO NAME month_name VALUE val)
WHERE TRY_CAST(val AS DOUBLE) IS NOT NULL
""").fetchall())

# dynamic unpivot (LAUS) - columns drift
con.execute("""
create table laus as select * from (values
  ('7','CA09','Bridgeport','Labor Force','1018606','1019596')
) t(method,area_code,area_title,data_type,jan_2024_r_,feb_2024_r_)
""")
print("LAUS dynamic unpivot:")
print(con.execute("""
SELECT area_code, area_title, data_type, method, period,
       TRY_CAST(REPLACE(value,',','') AS DOUBLE) AS value
FROM (UNPIVOT laus
      ON COLUMNS(* EXCLUDE (method, area_code, area_title, data_type))
      INTO NAME period VALUE value)
WHERE value IS NOT NULL AND value <> ''
""").fetchall())

# comma/percent cleaning (CES current)
print("clean numbers:")
print(con.execute("""
SELECT TRY_CAST(REPLACE('11,600',',','') AS DOUBLE),
       TRY_CAST(REPLACE(REPLACE('0.67%','%',''),',','') AS DOUBLE)
""").fetchall())
