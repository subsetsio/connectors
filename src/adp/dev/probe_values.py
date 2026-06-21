import csv, io, zipfile, httpx, statistics as st
def read(idx):
    j = httpx.get(idx, timeout=60).json()
    raw = httpx.get(j["reportDownloadLink"], timeout=120).content
    zf = zipfile.ZipFile(io.BytesIO(raw))
    name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
    return list(csv.DictReader(io.StringIO(zf.read(name).decode("utf-8"))))
def stats(rows, col):
    v = [float(r[col]) for r in rows if r[col].strip()]
    v.sort()
    n = len(v)
    print(f"  {col}: n={n} nulls={len(rows)-n} min={v[0]:.3f} max={v[-1]:.3f} median={st.median(v):.3f}")
ner = read("https://adpemploymentreport.com/ner_production.json")
print("NER")
for c in ("NER","NER_SA"): stats(ner,c)
# National monthly subset value
nat = [r for r in ner if r["agg_RIS"]=="National" and r["timestep"]=="M"]
import statistics
vv=sorted(float(r["NER"]) for r in nat if r["NER"].strip())
print("  National M NER:", vv[0], "->", vv[-1])
pay = read("https://payinsights.adp.com/pay_insights_production.json")
print("PAY")
for c in ("median pay change","median annual pay"): stats(pay,c)
