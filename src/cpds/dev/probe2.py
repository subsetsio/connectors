from subsets_utils import get
html = get("https://cpds-data.org/data/", timeout=60).text
print("len html:", len(html))
import re
for ext in ("xlsx","dta","zip","pdf"):
    print(ext, "count:", len(re.findall(r'\.'+ext, html)))
# print all hrefs containing uploads
for m in re.findall(r'href="([^"]+)"', html):
    if "upload" in m or "xls" in m or ".dta" in m:
        print(" HREF:", m)
