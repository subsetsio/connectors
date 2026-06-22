import io, json, duckdb, pyarrow as pa
from subsets_utils import io as sio
from utils import build_groups, datastore_rows

ENTITIES = [
    "taxation-statistics--financialratios4trusts1c-csv",   # multi-year, consistent cols
    "self-managed-superannuation-funds--smsf-quarterly-statistical-report-june",
    "corporate-transparency--report-of-entity-tax-information",  # non-yearly, income_year null
    "taxation-statistics-postcode-data--income-year-all-individuals",
]
groups = build_groups()
for ent in ENTITIES:
    res = groups.get(ent)
    print("\n===", ent, "->", len(res) if res else None, "resources")
    rows=[]; keys={}
    for r in res:
        if not r["datastore_active"]: continue
        for row in datastore_rows(r["resource_id"], r["income_year"]):
            rows.append(row); [keys.setdefault(k,None) for k in row]
    cols=list(keys)
    norm=[{k:row.get(k) for k in cols} for row in rows]
    # write to an in-memory ndjson, read back with read_json_auto exactly like runtime
    buf=io.BytesIO()
    for row in norm:
        buf.write(json.dumps(row, separators=(",",":")).encode()); buf.write(b"\n")
    data=buf.getvalue()
    open("/tmp/_one.ndjson","wb").write(data)
    print("rows", len(norm), "cols", cols[:12])
    t=duckdb.sql("SELECT * FROM read_json_auto('/tmp/_one.ndjson')")
    rb=t.fetch_record_batch(); first=next(iter(rb)) if rows else None
    res2=duckdb.sql("SELECT count(*) c FROM read_json_auto('/tmp/_one.ndjson')").fetchone()
    print("duckdb SELECT * count:", res2[0])
    print("duckdb schema:", duckdb.sql("DESCRIBE SELECT * FROM read_json_auto('/tmp/_one.ndjson')").fetchall()[:6])
