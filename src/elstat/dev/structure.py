import re
from subsets_utils import get
html = get("https://www.statistics.gr/en/statistics/-/publication/SDT03/-", timeout=(10,60)).text
# find the documents portlet section; print a window around documentID occurrences
for m in re.finditer(r'documentID=(\d+)', html):
    i = m.start()
    seg = html[i-400:i+80]
    seg = re.sub(r'\s+', ' ', seg)
    print("DOCID", m.group(1))
    print("  ...", seg[-380:])
    print()
