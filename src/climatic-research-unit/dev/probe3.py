from subsets_utils import get
import re
base = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.09/"
r = get(base, timeout=(10,60)); r.raise_for_status()
print("STATUS", r.status_code, "len", len(r.text))
# print all hrefs
hrefs = re.findall(r'href="([^"]+)"', r.text)
for h in hrefs: print(repr(h))
