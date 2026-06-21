import json, duckdb, urllib.request
# reuse already-downloaded /tmp files to avoid refetch
import sys
maps = {
 "efw":"/tmp/ftw_get_all_data.json",
 "allgov":"/tmp/ftw_get_states_data.json",
 "subnat":"/tmp/ftw_get_subnational_data.json",
}
def flatten(payload):
    rows=[]
    for ys,recs in payload.items():
        y=int(ys)
        for rec in recs:
            row={"year":y}
            for k,v in rec.items():
                if isinstance(v,dict): row[k.lower()]=v.get("value")
                else: row[k]=v
            rows.append(row)
    return rows
con=duckdb.connect()
for name,f in maps.items():
    rows=flatten(json.load(open(f)))
    con.register(name, duckdb.from_arrow.__self__.values if False else None) or None
    # write ndjson temp and read
    p=f"/tmp/{name}.ndjson"
    with open(p,"w") as fh:
        for r in rows: fh.write(json.dumps(r)+"\n")
SQL = {
"efw": '''SELECT CAST(year AS INTEGER) year, country, iso_code,
 TRY_CAST(summary_index AS DOUBLE) economic_freedom_summary,
 TRY_CAST(rank AS INTEGER) world_rank, TRY_CAST(quartile AS INTEGER) quartile,
 TRY_CAST(area1 AS DOUBLE) size_of_government, TRY_CAST(area1rank AS INTEGER) sog_rank,
 TRY_CAST(area5 AS DOUBLE) regulation
 FROM read_json_auto('/tmp/efw.ndjson') WHERE iso_code IS NOT NULL AND iso_code<>'' ''',
"allgov": '''SELECT CAST(year AS INTEGER) year, country, state_province, iso_code, type jt,
 TRY_CAST(summary_index AS DOUBLE) efs, TRY_CAST(rank AS INTEGER) rank,
 TRY_CAST(area6 AS DOUBLE) trade FROM read_json_auto('/tmp/allgov.ndjson') WHERE iso_code IS NOT NULL AND iso_code<>'' ''',
"subnat": '''SELECT CAST(year AS INTEGER) year, country, state_province, iso_code,
 TRY_CAST(area3 AS DOUBLE) labor FROM read_json_auto('/tmp/subnat.ndjson') WHERE iso_code IS NOT NULL AND iso_code<>'' ''',
}
for name,sql in SQL.items():
    r=con.execute(sql).arrow()
    print(name, "rows", r.num_rows, "cols", r.num_columns,
          "| years", con.execute(f"SELECT min(year),max(year),count(distinct year) FROM ({sql})").fetchone(),
          "| dup(year,iso)", con.execute(f"SELECT count(*)-count(distinct (year||iso_code)) FROM ({sql})").fetchone()[0])
