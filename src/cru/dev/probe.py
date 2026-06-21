import re
from subsets_utils import get

BASE = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/crucy.2503061057.v4.09/countries"

# 1) variable dir index -> .per filenames
html = get(f"{BASE}/tmp/", timeout=(10, 60)).text
files = re.findall(r'href="(crucy\.[^"]+\.per)"', html)
print("tmp files:", len(files), files[:3])

# 2) one .per file
txt = get(f"{BASE}/tmp/{files[0]}", timeout=(10, 60)).text
lines = txt.splitlines()
for ln in lines[:5]:
    print(repr(ln))
print("...total lines:", len(lines))
# header detection
hdr_idx = next(i for i, l in enumerate(lines) if l.strip().startswith("YEAR"))
print("header idx:", hdr_idx, "cols:", lines[hdr_idx].split())
print("first data row split:", lines[hdr_idx + 1].split())
print("last data row:", lines[-1].split())
