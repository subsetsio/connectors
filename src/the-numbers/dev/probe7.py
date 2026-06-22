import sys
sys.path.insert(0, "src")
from nodes import the_numbers as N

# 1) parse a daily page
for kind in ["daily", "weekend", "weekly"]:
    newest = N._find_newest(kind)
    print(f"{kind}: newest =", newest)
    html = N._get_html(N._path(kind, newest))
    rows, prev, nxt = N._parse_chart(html, kind, newest)
    print(f"  rows={len(rows)} prev={prev} next={nxt}")
    print("  sample:", rows[0])

# 2) walk 3 daily pages backward to confirm chaining
print("---- daily backward chain ----")
cur = N._find_newest("daily")
for _ in range(3):
    html = N._get_html(N._path("daily", cur))
    rows, prev, nxt = N._parse_chart(html, "daily", cur)
    print(f"  {cur}: {len(rows)} rows, prev={prev}")
    cur = prev

# 3) annual parse for two years
for y in [2025, 1995, 1994]:
    html = N._get_html(f"/market/{y}/top-grossing-movies")
    rows = N._parse_annual(html, y) if html else []
    print(f"annual {y}: {len(rows)} rows", rows[0] if rows else "")
