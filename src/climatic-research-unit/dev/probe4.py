from subsets_utils import get
import re
base = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/"
r = get(base, timeout=(10,60)); r.raise_for_status()
cydirs = re.findall(r'href="(crucy\.[^"/]+)"', r.text)
print("crucy dirs:", cydirs)
cydir = base + cydirs[0] + "/countries/"
r2 = get(cydir, timeout=(10,60)); r2.raise_for_status()
print("--- countries/ hrefs ---")
hrefs = re.findall(r'href="([^"]+)"', r2.text)
for h in hrefs: print(repr(h))
