from subsets_utils import get
import re
r = get("https://cpds-data.org/data/", timeout=60)
html = r.text
print("len:", len(html))
hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
for h in hrefs:
    if any(x in h.lower() for x in (".xlsx",".dta",".zip",".pdf","upload")):
        print(h)
