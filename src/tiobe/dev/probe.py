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

def rows_of(tid):
    return doc.get_element_by_id(tid).findall(".//tr")

def tds(tr):
    return tr.findall("td")

def ths(tr):
    return tr.findall("th")

# --- top20 ---
rows = rows_of("top20")
print("\n# top20 rows:", len(rows))
for tr in rows[1:4]:
    print([cell_text(c) for c in tds(tr)])

# --- otherPL ---
rows = rows_of("otherPL")
print("\n# otherPL rows:", len(rows))
for tr in rows[1:3]:
    print([cell_text(c) for c in tds(tr)])

# --- VLTH ---
rows = rows_of("VLTH")
header = [cell_text(c) for c in ths(rows[0])]
print("\n# VLTH header:", header)
for tr in rows[1:3]:
    print([cell_text(c) for c in tds(tr)])

# --- PLHoF ---
print("\n# PLHoF rows:")
for tr in rows_of("PLHoF"):
    cells = tds(tr)
    if len(cells) >= 2:
        print(cell_text(cells[0]), "|", cell_text(cells[1]))

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
