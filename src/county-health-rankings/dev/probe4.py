import sys, csv, io
sys.path.insert(0, "src/nodes")
import importlib.util
spec = importlib.util.spec_from_file_location("chr", "src/nodes/county_health_rankings.py")
chr = importlib.util.module_from_spec(spec); spec.loader.exec_module(chr)

# analytic single year parse
txt = chr._fetch_text("https://www.countyhealthrankings.org/sites/default/files/media/document/analytic_data2025_v3.csv")
rows = list(chr._parse_analytic(txt))
print("2025 analytic long rows:", len(rows))
print("sample:", rows[0])
# distinct measures + a known one
ms = {(r['measure_id'], r['measure_name']) for r in rows}
print("distinct measures:", len(ms))
print("sample measures:", sorted(ms)[:5])
pd = [r for r in rows if r['measure_id']==1][:2]
print("measure_id=1 sample:", pd)

# trends parse: just header check + count via discover
files = chr._discover(r"chr_trends_csv_(\d{4})")
print("trends files:", files)
