import csv, io, zipfile, httpx, collections
def read(idx):
    j = httpx.get(idx, timeout=60).json()
    raw = httpx.get(j["reportDownloadLink"], timeout=120).content
    zf = zipfile.ZipFile(io.BytesIO(raw))
    name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
    rows = list(csv.DictReader(io.StringIO(zf.read(name).decode("utf-8"))))
    return rows
for label, idx, aggkey in [
    ("NER", "https://adpemploymentreport.com/ner_production.json", "agg_RIS"),
    ("PAY", "https://payinsights.adp.com/pay_insights_production.json", "agg"),
]:
    rows = read(idx)
    print("="*60, label, "rows=", len(rows))
    print("cols:", list(rows[0].keys()))
    for col in ("timestep", aggkey, "category"):
        c = collections.Counter(r[col] for r in rows)
        print(f"  {col}: {len(c)} distinct ->", dict(list(c.most_common(12))))
    dates = sorted(r["date"] for r in rows)
    print("  date range:", dates[0], "->", dates[-1])
