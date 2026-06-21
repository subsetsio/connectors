import io, json, tempfile, os
import duckdb, openpyxl
from datetime import datetime, timezone
from subsets_utils import get

def ndjson_view(con, name, rows):
    f = tempfile.NamedTemporaryFile("w", suffix=".ndjson", delete=False)
    for r in rows: f.write(json.dumps(r)+"\n")
    f.close()
    con.execute(f"""CREATE VIEW "{name}" AS SELECT * FROM read_ndjson_auto('{f.name}')""")

con = duckdb.connect()

# GSoD indices
y2 = datetime.now(tz=timezone.utc).year + 1
gi = get("https://www.idea.int/gsod-indices/api/data", params={"year1":1900,"year2":y2}, timeout=180).json()
print("gsod rows", len(gi))
ndjson_view(con, "international-idea-gsod-indices", gi)
r = con.execute('''
    SELECT CAST(ID_country_code AS INTEGER) AS country_code, ID_country_name AS country_name,
           CAST(ID_year AS INTEGER) AS year, TRY_CAST(ID_region AS INTEGER) AS region_id,
           TRY_CAST(ID_subregion AS INTEGER) AS subregion_id, TRY_CAST(regime AS INTEGER) AS regime,
           TRY_CAST(dem AS INTEGER) AS dem_performance_band, TRY_CAST(demperf AS INTEGER) AS dem_performance,
           TRY_CAST(COLUMNS('^(A|SA|SC)_') AS DOUBLE)
    FROM "international-idea-gsod-indices"
    WHERE ID_year IS NOT NULL AND ID_country_code IS NOT NULL
''').fetch_arrow_table()
print("gsod transform: rows", r.num_rows, "cols", r.num_columns)
print("  year range", con.execute('SELECT min(year),max(year) FROM r').fetchall() if False else (min(r.column('year').to_pylist()), max(r.column('year').to_pylist())))
print("  A_01 sample", r.column('A_01').to_pylist()[0] if 'A_01' in r.column_names else 'MISSING')

# Indicators
ind = get("https://www.idea.int/gsod-indices/api/labels", timeout=60).json()
ndjson_view(con, "international-idea-gsod-indicators", ind)
ri = con.execute('''SELECT id AS indicator_code, name AS indicator_name, description, section AS parent_code,
    color, selectable, TRY_CAST("Weight" AS DOUBLE) AS weight
    FROM "international-idea-gsod-indicators" WHERE id IS NOT NULL''').fetch_arrow_table()
print("indicators transform: rows", ri.num_rows, "cols", ri.column_names)

# Voter turnout
resp = get("https://www.idea.int/data-tools/export", params={"type":"region_only","themeId":293,"world":"all","loc":"home"}, timeout=120)
wb = openpyxl.load_workbook(io.BytesIO(resp.content), read_only=True, data_only=True)
ws = wb["All"]; itr = ws.iter_rows(values_only=True)
header=[str(h).strip() for h in next(itr)]; vt=[]
for raw in itr:
    if all(c is None for c in raw): continue
    vt.append({header[i]:(None if (i>=len(raw) or raw[i] is None) else str(raw[i])) for i in range(len(header))})
wb.close()
print("vt rows", len(vt))
ndjson_view(con, "international-idea-voter-turnout", vt)
rv = con.execute('''SELECT "Country" AS country, "ISO2" AS iso2, "ISO3" AS iso3, "Election Type" AS election_type,
    TRY_CAST("Year" AS DATE) AS election_date,
    TRY_CAST(REPLACE(CAST("Voter Turnout" AS VARCHAR),'%','') AS DOUBLE) AS voter_turnout_pct,
    TRY_CAST(REPLACE(CAST("Total vote" AS VARCHAR),',','') AS BIGINT) AS total_vote,
    TRY_CAST(REPLACE(CAST("Registration" AS VARCHAR),',','') AS BIGINT) AS registration,
    TRY_CAST(REPLACE(CAST("VAP Turnout" AS VARCHAR),'%','') AS DOUBLE) AS vap_turnout_pct,
    TRY_CAST(REPLACE(CAST("Voting age population" AS VARCHAR),',','') AS BIGINT) AS voting_age_population,
    TRY_CAST(REPLACE(CAST("Population" AS VARCHAR),',','') AS BIGINT) AS population,
    TRY_CAST(REPLACE(CAST("Invalid votes" AS VARCHAR),'%','') AS DOUBLE) AS invalid_votes_pct,
    "Compulsory voting" AS compulsory_voting
    FROM "international-idea-voter-turnout" WHERE "Country" IS NOT NULL''').fetch_arrow_table()
print("vt transform: rows", rv.num_rows)
import pyarrow.compute as pc
nd = pc.sum(pc.is_valid(rv.column('election_date'))).as_py()
print("  non-null election_date", nd, "/", rv.num_rows)
print("  sample turnout", rv.column('voter_turnout_pct').to_pylist()[0], "total_vote", rv.column('total_vote').to_pylist()[0])
print("OK ALL THREE")
