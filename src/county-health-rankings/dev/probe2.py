from subsets_utils import get

years = {
  "2010": "/sites/default/files/analytic_data2010.csv",
  "2015": "/sites/default/files/analytic_data2015.csv",
  "2020": "/sites/default/files/media/document/analytic_data2020_0.csv",
  "2025": "/sites/default/files/media/document/analytic_data2025_v3.csv",
}
for yr, path in years.items():
    url = "https://www.countyhealthrankings.org" + path
    r = get(url, headers={"Range": "bytes=0-6000"}, timeout=(10,60))
    txt = r.content.decode("utf-8", errors="replace")
    lines = txt.splitlines()
    h = lines[0].split(",")
    raw = [c for c in h if c.endswith(" raw value")]
    print(f"=== {yr} status={r.status_code} cols(chunk)={len(h)}")
    print("  first 10:", h[:10])
    print("  raw-value cols in chunk:", raw[:5])
    print("  line2:", lines[1][:160] if len(lines)>1 else "NONE")
