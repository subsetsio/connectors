import re
from subsets_utils import get

pages = [
    "https://www.countyhealthrankings.org/health-data/methodology-and-sources/data-documentation",
    "https://www.countyhealthrankings.org/health-data/methodology-and-sources/data-documentation/national-data-documentation-2010-2023",
]
links = set()
for p in pages:
    r = get(p, timeout=(10,60)); r.raise_for_status()
    for m in re.findall(r'href="([^"]+)"', r.text):
        if re.search(r'analytic[_ ]?data', m, re.I) and m.lower().endswith('.csv'):
            links.add(m)
        if re.search(r'chr_trends_csv', m, re.I) and m.lower().endswith('.csv'):
            links.add(m)
for l in sorted(links):
    print(l)
