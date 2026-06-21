from subsets_utils import get

# 1. Temperature time-series format
url = "https://crudata.uea.ac.uk/cru/data/temperature/HadCRUT5.1Analysis_gl.txt"
r = get(url, timeout=(10,60)); r.raise_for_status()
lines = r.text.splitlines()
print("=== HadCRUT5.1Analysis_gl.txt ===")
print("n_lines:", len(lines))
for ln in lines[:6]: print(repr(ln))
print("... last 4 ...")
for ln in lines[-4:]: print(repr(ln))
# token counts
import collections
tc = collections.Counter(len(ln.split()) for ln in lines if ln.strip())
print("token-count distribution:", dict(tc))
