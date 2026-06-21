from subsets_utils import get
import re
cydir = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/crucy.2503061057.v4.09/countries/"
tmp = cydir + "tmp/"
r = get(tmp, timeout=(10,60)); r.raise_for_status()
files = re.findall(r'href="([^"]+\.per)"', r.text)
print("n .per files in tmp:", len(files))
print("sample:", files[:6])
# fetch one
furl = tmp + files[0]
r2 = get(furl, timeout=(10,60)); r2.raise_for_status()
lines = r2.text.splitlines()
print("=== file:", files[0], " n_lines:", len(lines))
for ln in lines[:14]: print(repr(ln))
print("...last 3...")
for ln in lines[-3:]: print(repr(ln))
