from subsets_utils import get
import re

# Resolve current crucy timestamped dir under cru_ts_4.09
base = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/"
r = get(base, timeout=(10,60)); r.raise_for_status()
dirs = re.findall(r'href="(crucy\.[^"/]+/)"', r.text)
print("crucy dirs:", dirs)

cydir = base + dirs[0] + "countries/"
r2 = get(cydir, timeout=(10,60)); r2.raise_for_status()
varlinks = re.findall(r'href="([^"/]+/)"', r2.text)
print("var subdirs:", varlinks)

# list tmp dir country files
tmpdir = cydir + "tmp/"
r3 = get(tmpdir, timeout=(10,60)); r3.raise_for_status()
files = re.findall(r'href="([^"]+\.per)"', r3.text)
print("n country files in tmp:", len(files))
print("sample files:", files[:5])

# fetch one country file
furl = tmpdir + files[0]
r4 = get(furl, timeout=(10,60)); r4.raise_for_status()
lines = r4.text.splitlines()
print("=== sample .per file:", files[0], "===")
print("n_lines:", len(lines))
for ln in lines[:12]: print(repr(ln))
print("... last 3 ...")
for ln in lines[-3:]: print(repr(ln))
