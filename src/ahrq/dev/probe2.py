import duckdb, time, resource
con = duckdb.connect()
con.execute("INSTALL excel; LOAD excel;")
t=time.time()
con.execute("CREATE TABLE t AS SELECT * FROM read_xlsx('/tmp/h251.xlsx', all_varchar=true)")
n=con.execute("SELECT count(*) FROM t").fetchone()[0]
cols=con.execute("PRAGMA table_info('t')").fetchall()
print("rows",n,"cols",len(cols),"secs",round(time.time()-t,1))
print("first cols:",[c[1] for c in cols[:8]])
# write to parquet to check size
con.execute("COPY t TO '/tmp/h251.parquet' (FORMAT parquet, COMPRESSION zstd)")
import os; print("parquet MB", round(os.path.getsize('/tmp/h251.parquet')/1e6,1))
print("peak RSS MB", round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6,0))
