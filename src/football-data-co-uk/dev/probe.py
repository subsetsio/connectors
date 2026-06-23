import re
from subsets_utils import get

# Discover the link structure from the main data page
r = get("https://www.football-data.co.uk/data.php", timeout=(10,60))
html = r.text
mmz = sorted(set(re.findall(r'(mmz4281/\d{4}/[A-Z0-9]+\.csv)', html)))
new = sorted(set(re.findall(r'(new/[A-Z0-9]+\.csv)', html)))
print("data.php status", r.status_code, "len", len(html))
print("mmz links on data.php:", len(mmz), mmz[:10])
print("new links on data.php:", len(new), new)

# country page (england)
r2 = get("https://www.football-data.co.uk/englandm.php", timeout=(10,60))
mmz2 = sorted(set(re.findall(r'(mmz4281/\d{4}/[A-Z0-9]+\.csv)', r2.text)))
print("\nenglandm.php mmz links:", len(mmz2), mmz2[:15])
divs = sorted(set(m.split('/')[-1][:-4] for m in mmz2))
seasons = sorted(set(m.split('/')[1] for m in mmz2))
print("england divisions:", divs)
print("england seasons:", seasons[:5], "...", seasons[-3:])
