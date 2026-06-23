import re
from subsets_utils import get

r = get("https://www.football-data.co.uk/data.php", timeout=(10,60))
html = r.text
phps = sorted(set(re.findall(r'href="([a-zA-Z]+\.php)"', html)))
print("php pages linked from data.php:", phps)

# The extra/new leagues are typically listed on a page; find any new/ links across candidate pages
for page in phps:
    try:
        rr = get(f"https://www.football-data.co.uk/{page}", timeout=(10,60))
        new = sorted(set(re.findall(r'(new/[A-Z0-9]+\.csv)', rr.text)))
        mmz = sorted(set(re.findall(r'mmz4281/\d{4}/([A-Z0-9]+)\.csv', rr.text)))
        if new or mmz:
            print(f"{page}: new={new} divisions={sorted(set(mmz))}")
    except Exception as e:
        print(page, "ERR", e)
