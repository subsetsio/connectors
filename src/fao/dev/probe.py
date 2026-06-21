import io
import zipfile
import json
from subsets_utils import get

MANIFEST = "https://bulks-faostat.fao.org/production/datasets_E.json"

m = get(MANIFEST, timeout=(10, 60))
datasets = m.json()["Datasets"]["Dataset"]
by_code = {d["DatasetCode"]: d for d in datasets}

# small domain to download fully; others header-only
SMALL = "MDDW"
DIVERSE = ["QCL", "TM", "CP", "SDGB", "PE"]

print("=== manifest record sample (MDDW) ===")
print(json.dumps(by_code[SMALL], indent=2)[:1500])

def inspect(code, full=False):
    rec = by_code[code]
    url = rec["FileLocation"]
    print(f"\n=== {code}  {rec['DatasetName'][:60]}  rows={rec['FileRows']} size={rec['FileSize']} ===")
    print("url:", url)
    # range request: just grab enough bytes for small; full for SMALL
    if full:
        data = get(url, timeout=(10, 300)).content
    else:
        # grab whole zip only if small enough; else first 2MB won't give a valid zip (central dir at end)
        data = get(url, timeout=(10, 300)).content
    print("zip bytes:", len(data))
    zf = zipfile.ZipFile(io.BytesIO(data))
    names = zf.namelist()
    print("members:", names)
    main = [n for n in names if n.lower().endswith("(normalized).csv")]
    print("main normalized member:", main)
    target = main[0] if main else names[0]
    raw = zf.read(target)
    # encoding check
    try:
        raw[:200000].decode("utf-8")
        enc = "utf-8 ok (first 200k)"
    except UnicodeDecodeError as e:
        enc = f"NOT utf-8: {e}"
    print("encoding:", enc)
    text = raw.decode("latin-1")
    lines = text.splitlines()
    print("header:", lines[0])
    print("row1:", lines[1] if len(lines) > 1 else "")
    print("row2:", lines[2] if len(lines) > 2 else "")

inspect(SMALL, full=True)
for c in DIVERSE:
    try:
        inspect(c)
    except Exception as e:
        print(f"{c} failed: {type(e).__name__}: {e}")
