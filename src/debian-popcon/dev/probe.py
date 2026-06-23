import gzip
from subsets_utils import get

for path in ["by_inst.gz", "source/by_inst.gz", "sourcemax/by_inst.gz", "maint/by_inst.gz"]:
    url = f"https://popcon.debian.org/{path}"
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    text = gzip.decompress(r.content).decode("utf-8", "replace")
    lines = text.splitlines()
    print("=" * 70)
    print(url, "->", len(lines), "lines,", len(r.content), "bytes gz")
    # show header lines and first/last data rows
    for ln in lines[:16]:
        print(repr(ln))
    print("...last 3 data lines...")
    for ln in lines[-3:]:
        print(repr(ln))
