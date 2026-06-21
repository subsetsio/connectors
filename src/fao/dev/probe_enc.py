import io, zipfile, json
from subsets_utils import get

m = get("https://bulks-faostat.fao.org/production/datasets_E.json", timeout=(10, 60)).json()
by = {d["DatasetCode"]: d for d in m["Datasets"]["Dataset"]}

for code in ["CBH", "FBSH", "FT", "PA", "RA", "RM", "RY"]:
    rec = by.get(code)
    if not rec:
        print(code, "NOT IN MANIFEST"); continue
    data = get(rec["FileLocation"], timeout=(10, 300)).content
    zf = zipfile.ZipFile(io.BytesIO(data))
    member = [n for n in zf.namelist() if n.lower().endswith("(normalized).csv")][0]
    raw = zf.read(member)
    # find first invalid utf-8 byte
    try:
        raw.decode("utf-8")
        verdict = "valid utf-8"
        ctx = ""
    except UnicodeDecodeError as e:
        verdict = f"INVALID utf-8 @ byte {e.start}: {raw[e.start:e.start+1]!r}"
        seg = raw[max(0, e.start-30):e.start+30]
        ctx = f" cp1252={seg.decode('cp1252', 'replace')!r} latin1={seg.decode('latin-1')!r}"
    print(f"{code}: rows={rec['FileRows']} {verdict}{ctx}")
