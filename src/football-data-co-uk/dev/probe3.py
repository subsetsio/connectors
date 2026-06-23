import re
from subsets_utils import get
r = get("https://www.football-data.co.uk/data.php", timeout=(10,60))
html = r.text
allhref = sorted(set(re.findall(r'href=["\']?([^"\'> ]+\.php)', html, re.I)))
print("all .php hrefs:", allhref)
newhref = sorted(set(re.findall(r'(new/[A-Za-z0-9]+\.csv)', html)))
print("new csv on data.php:", newhref)
# show any line containing 'new/' or 'csv'
for m in re.findall(r'.{0,40}new/.{0,40}', html):
    print("CTX:", m)
