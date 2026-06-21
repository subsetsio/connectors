import duckdb, pyarrow as pa
# simulate long-format raw for the 'prices' dataset
rows = [
    ("2021-01-01","pct_higher",64.3),("2021-01-01","index",82.1),("2021-01-01","net",64.3),
    ("2021-02-01","pct_higher",60.0),("2021-02-01","index",80.0),("2021-02-01","net",60.0),
]
t = pa.table({"date":[r[0] for r in rows],"metric":[r[1] for r in rows],"value":[r[2] for r in rows]})
con = duckdb.connect()
con.register("ism-prices", t)
sql = '''
PIVOT (SELECT CAST(date AS DATE) AS date, metric, value FROM "ism-prices")
ON metric USING first(value)
GROUP BY date
ORDER BY date
'''
res = con.execute(sql).arrow().read_all()
print("cols:", res.column_names)
print(res.to_pydict())
# single-series case
t2 = pa.table({"date":["2020-05-01","2020-06-01"],"metric":["pmi","pmi"],"value":[43.1,52.2]})
con.register("ism-pmi", t2)
res2 = con.execute('PIVOT (SELECT CAST(date AS DATE) AS date, metric, value FROM "ism-pmi") ON metric USING first(value) GROUP BY date ORDER BY date').arrow().read_all()
print("pmi cols:", res2.column_names, res2.to_pydict())
