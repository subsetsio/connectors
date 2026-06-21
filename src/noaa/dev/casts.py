import duckdb
con = duckdb.connect()
# NESIS-style date m/d/Y, RSI date Y-m-d, storm make_date, ibtracs timestamp
q = """
SELECT
  try_strptime('3/12/1993', '%m/%d/%Y')::DATE              AS nesis_date,
  try_strptime('12/6/1996', '%m/%d/%Y')::DATE             AS nesis_date2,
  CAST('2013-03-04' AS DATE)                              AS rsi_date,
  make_date(CAST(substr('202006',1,4) AS INT), CAST(substr('202006',5,2) AS INT), 24) AS se_date,
  CAST('2020-06-24 16:20:00' AS TIMESTAMP)               AS ts,
  regexp_replace('1°','[^0-9]','','g')::INT          AS rank_clean,
  TRY_CAST('' AS DOUBLE)                                  AS empty_dbl,
  TRY_CAST('50.00' AS DOUBLE)                             AS wind
"""
print(con.execute(q).fetchall())
print([d[0] for d in con.description])
