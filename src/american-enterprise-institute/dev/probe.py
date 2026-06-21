from subsets_utils import get
import re

PAGE = "https://www.aei.org/national-and-metro-housing-market-indicators/"
r = get(PAGE, timeout=(10,120))
print("page status", r.status_code, "len", len(r.text))
# find xlsx links
links = re.findall(r'href="([^"]+\.xlsx[^"]*)"', r.text)
for l in links:
    print("XLSX:", l)
