import sys, io, csv
sys.path.insert(0, "src")
import pyarrow as pa, duckdb
from nodes.bioconductor import _parse_dcf, _fetch_text, PACKAGE_FIELDS, VIEWS_REPOS

# 1) packages: parse live VIEWS for one small repo (workflows) end-to-end
text = _fetch_text("https://bioconductor.org/packages/release/workflows/VIEWS")
recs = [r for r in _parse_dcf(text) if "Package" in r]
print("workflows packages parsed:", len(recs))
print("sample fields:", {k: recs[0].get(k) for k in ["Package","Version","Title","biocViews","Date/Publication","git_last_commit_date"]})
missing_version = sum(1 for r in recs if not r.get("Version"))
print("missing Version:", missing_version)

# 2) downloads transform SQL against a synthetic sample (verified .tab format)
sample = [
    {"package":"DESeq2","repo":"bioc","year":2026,"month":"Jan","distinct_ips":1000,"downloads":2500},
    {"package":"DESeq2","repo":"bioc","year":2026,"month":"all","distinct_ips":12000,"downloads":30000},
    {"package":"a4","repo":"bioc","year":2009,"month":"Dec","distinct_ips":5,"downloads":7},
]
schema = pa.schema([("package",pa.string()),("repo",pa.string()),("year",pa.int32()),
                    ("month",pa.string()),("distinct_ips",pa.int64()),("downloads",pa.int64())])
t = pa.Table.from_pylist(sample, schema=schema)
con = duckdb.connect()
con.register("bioconductor-downloads", t)
sql = '''
    SELECT make_date(CAST(year AS INTEGER), m.month_num, 1) AS date, package, repo,
           CAST(year AS INTEGER) AS year, m.month_num AS month,
           CAST(distinct_ips AS BIGINT) AS distinct_ips, CAST(downloads AS BIGINT) AS downloads
    FROM "bioconductor-downloads"
    JOIN (VALUES ('Jan',1),('Feb',2),('Mar',3),('Apr',4),('May',5),('Jun',6),
                 ('Jul',7),('Aug',8),('Sep',9),('Oct',10),('Nov',11),('Dec',12))
         AS m(month_abbr, month_num) ON month = m.month_abbr
'''
out = con.execute(sql).fetchall()
print("downloads transform rows (should be 2, 'all' dropped):", len(out))
for r in out: print("  ", r)

# 3) packages transform date casts
pt = pa.table({"package":["x"],"repo":["bioc"],"version":["1.0"],"title":["t"],
    "description":["d"],"biocviews":["Microarray"],"license":["GPL-3"],"maintainer":["m"],
    "depends":[None],"imports":[None],"needs_compilation":["no"],
    "git_last_commit_date":["2026-04-28"],"date_publication":["2026-05-05"]})
con.register("bioconductor-packages", pt)
out2 = con.execute('''SELECT TRY_CAST(git_last_commit_date AS DATE) g, TRY_CAST(date_publication AS DATE) d
                      FROM "bioconductor-packages"''').fetchall()
print("packages date casts:", out2)
