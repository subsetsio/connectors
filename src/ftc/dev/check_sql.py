import csv, io, re, json, tempfile, os
import duckdb
from subsets_utils import get

BASE = "https://www.ftc.gov"
DATASETS = BASE + "/policy-notices/open-government/data-sets"

def parse(url):
    raw = get(url, timeout=(10, 120)).content
    rows = []
    for rec in csv.DictReader(io.StringIO(raw.decode("cp1252", errors="replace"))):
        rows.append({(k.strip() if k else k): (v.strip() if isinstance(v, str) else v)
                     for k, v in rec.items() if k is not None})
    return rows

def ndjson_tmp(rows):
    fd, path = tempfile.mkstemp(suffix=".ndjson")
    with os.fdopen(fd, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return path

html = get(DATASETS, timeout=(10, 120)).content.decode("utf-8", "replace")
hrefs = re.findall(r'href="([^"]*attachments/data-sets/[^"]+\.csv)"', html)

def url_for(slug):
    pat = re.compile(rf"/{re.escape(slug)}(?:_\d+)?\.csv$")
    return BASE + next(h for h in hrefs if "dictionary" not in h and pat.search(h))

con = duckdb.connect()

# merger (has spaced column + en-dash industry + date parsing)
merger = ndjson_tmp(parse(url_for("ftc_merger_enforcement_actions")))
con.execute(f"CREATE VIEW \"ftc-ftc-merger-enforcement-actions\" AS SELECT * FROM read_json_auto('{merger}')")
r = con.execute('''
    SELECT TRY_CAST(MatterEnforcementFY AS INTEGER) AS enforcement_fy,
           TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
           MatterName AS matter_name, MatterIndustry AS matter_industry,
           "Matter Enforcement Type" AS enforcement_type,
           NULLIF(trim(Matterhyperlink, '#'), '') AS url
    FROM "ftc-ftc-merger-enforcement-actions"
    WHERE MatterName IS NOT NULL AND MatterName <> ''
''').fetchall()
print("merger rows:", len(r))
print("merger sample:", r[0])
print("null dates:", con.execute('''SELECT count(*) FROM "ftc-ftc-merger-enforcement-actions" WHERE TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M') IS NULL AND MatterEnforcementDate <> '' ''').fetchone())

# hsr second requests (percent doubles)
hsr = ndjson_tmp(parse(url_for("hsr_transactions_filings_second_requests_by_fy")))
con.execute(f"CREATE VIEW v2 AS SELECT * FROM read_json_auto('{hsr}')")
r2 = con.execute('''SELECT TRY_CAST(FY AS INTEGER) fy, TRY_CAST(SecondRequestPercentFTC AS DOUBLE) p,
                    TRY_CAST(SecondRequestTotal AS INTEGER) t FROM v2''').fetchall()
print("hsr2 rows:", len(r2), "sample:", r2[0])
print("hsr2 null fy:", sum(1 for x in r2 if x[0] is None))
