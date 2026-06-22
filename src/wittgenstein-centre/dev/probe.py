import io, csv
from subsets_utils import get

REC = "https://zenodo.org/api/records/14718294"

def head(fname, n=4):
    url = f"{REC}/files/{fname}/content"
    r = get(url, timeout=(10, 180))
    r.raise_for_status()
    text = r.text
    lines = text.splitlines()
    print(f"\n=== {fname} === total_lines={len(lines)}")
    for ln in lines[:n]:
        print(ln)
    return lines

# small/medium files we can fully read
for f in ["MYS_AG_SSPs_V14.csv", "ASFR_AE_SSPs_V14.csv", "EDUprop_AGE_SSPs_V14.csv",
          "SX_AGE_SSPs_V14.csv", "SRB_SSPs_V14.csv"]:
    lines = head(f)
    # distinct of a few coded cols
    rdr = list(csv.DictReader(io.StringIO("\n".join(lines))))
    cols = rdr[0].keys() if rdr else []
    for c in ["sex", "agest", "Time"]:
        if c in cols:
            vals = sorted({row[c] for row in rdr})
            print(f"  distinct {c} ({len(vals)}): {vals[:30]}")

# recode dictionary - full var breakdown
rl = head("Recode dictionary.csv", n=2)
rrows = list(csv.DictReader(io.StringIO("\n".join(rl))))
from collections import Counter
print("  recode var counts:", Counter(r["var"] for r in rrows))
for v in sorted({r["var"] for r in rrows}):
    sample = [(r["varval"], r["varvaldesc"]) for r in rrows if r["var"] == v][:6]
    print(f"   var={v}: {sample}")
