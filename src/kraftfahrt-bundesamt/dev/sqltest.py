import duckdb, json
rows = [
  {"Berichtsjahr":"2020","Berichtsmonat":"Maerz","Anzahl":17,"ZS_Anzahl":None,"ObjectId":1,"Monat_Sortierung":3},
  {"Berichtsjahr":"2020","Berichtsmonat":"April","Anzahl":5,"ZS_Anzahl":"-","ObjectId":2,"Monat_Sortierung":4},
]
con = duckdb.connect()
con.execute("CREATE VIEW v AS SELECT * FROM read_json_auto(?)", ["/dev/stdin"]) if False else None
# write a temp ndjson
import tempfile, os
p = "/tmp/kba_sqltest.ndjson"
with open(p,"w") as f:
    for r in rows: f.write(json.dumps(r)+"\n")
con.execute(f"CREATE VIEW v AS SELECT * FROM read_json_auto('{p}')")
print("cols:", [c[0] for c in con.execute("DESCRIBE v").fetchall()])
sql = """
SELECT COLUMNS(c -> NOT regexp_matches(lower(c), '^(objectid|object_id|oid|fid|shape__|monat_sortierung)'))
FROM v
"""
res = con.execute(sql)
print("kept cols:", [d[0] for d in res.description])
print("rows:", con.execute(sql).fetchall())
