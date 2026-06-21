import duckdb, sys
print("duckdb", duckdb.__version__)
con = duckdb.connect()
try:
    con.execute("INSTALL excel; LOAD excel;")
    print("excel extension loaded")
except Exception as e:
    print("excel ext err:", e)
