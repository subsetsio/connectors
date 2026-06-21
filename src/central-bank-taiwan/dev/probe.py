import json
from subsets_utils import get

# Probe a spread of datasets across frequencies/categories to nail down:
# column ordering, period formats, missing-value tokens, structure-table counts.
CASES = ["EF01M01", "EF01Y01", "BP01D01", "BP01Y01", "EI75Y01", "FL01_cn", "BPP2Q01"]

for code in CASES:
    r = get(f"https://cpx.cbc.gov.tw/api/DataAPI/Get?FileName={code}", timeout=(10, 120))
    print("=" * 70)
    print(code, "HTTP", r.status_code, "ct", r.headers.get("content-type"))
    if r.status_code != 200:
        print("  body:", r.text[:80]); continue
    d = r.json()
    meta = d["meta"]; data = d["data"]
    struct = data["structure"]
    ds = data["dataSets"]
    dims = {k: [m["data"] for m in v] for k, v in struct.items()}
    n_value_cols = 1
    for v in dims.values():
        n_value_cols *= len(v)
    print("  title:", meta.get("title"))
    print("  units:", meta.get("units"), "| last_updated:", meta.get("last_updated"), "| matrix:", meta.get("matrix"))
    print("  structure:", {k: len(v) for k, v in dims.items()}, "=> value cols", n_value_cols, "+ period =", n_value_cols + 1)
    print("  actual cols in row0:", len(ds[0]))
    print("  periods: first", ds[0][0], "| last", ds[-1][0], "| n rows", len(ds))
    print("  row0:", ds[0][:8])
    # detect non-numeric value tokens
    toks = set()
    for row in ds[:50]:
        for c in row[1:]:
            try:
                float(c)
            except (ValueError, TypeError):
                toks.add(repr(c))
    print("  non-numeric value tokens (first 50 rows):", list(toks)[:10])
    # show dimension member labels
    for k, v in dims.items():
        print(f"    {k}: {v[:4]}{'...' if len(v) > 4 else ''}")
