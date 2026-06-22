import re
from subsets_utils import get

URL = "https://www.tiobe.com/tiobe-index/"
html = get(URL, timeout=(10.0, 120.0)).text
print("page bytes:", len(html))

import lxml.html as LH
doc = LH.fromstring(html)

def cell_text(td):
    return (td.text_content() or "").strip()

def pct(s):
    s = s.strip().replace("%", "").replace("+", "")
    return float(s) if s and s not in ("-",) else None

# --- top20 ---
rows = doc.cssselect("table#top20 tr")
print("\n# top20 rows:", len(rows))
for tr in rows[1:4]:
    tds = tr.cssselect("td")
    print([cell_text(c) for c in tds])

# --- otherPL ---
rows = doc.cssselect("table#otherPL tr")
print("\n# otherPL rows:", len(rows))
for tr in rows[1:3]:
    print([cell_text(c) for c in tr.cssselect("td")])

# --- VLTH ---
tbl = doc.cssselect("table#VLTH")[0]
header = [cell_text(c) for c in tbl.cssselect("tr")[0].cssselect("th")]
print("\n# VLTH header:", header)
for tr in tbl.cssselect("tr")[1:3]:
    print([cell_text(c) for c in tr.cssselect("td")])

# --- PLHoF ---
tbl = doc.cssselect("table#PLHoF")[0]
print("\n# PLHoF rows:")
for tr in tbl.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) >= 2:
        print(cell_text(tds[0]), "|", cell_text(tds[1]))
        break

# --- chart series ---
m = re.search(r"series:\s*\[(.*?)\]\s*\}\s*\)", html, re.S)
block = re.search(r"series:\s*\[(.*)", html, re.S).group(1)
names = re.findall(r"\{name : '([^']+)'", html)
print("\n# series names:", names)
pts = re.findall(r"\{name : '([^']+)',data : \[(.*?)\]\}", html, re.S)
print("# series parsed:", len(pts))
lang, data = pts[0]
tuples = re.findall(r"Date\.UTC\((\d+),\s*(\d+),\s*(\d+)\),\s*([\d.]+)", data)
print("#", lang, "points:", len(tuples), "first:", tuples[0], "last:", tuples[-1])
