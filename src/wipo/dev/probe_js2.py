import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import re
from subsets_utils import get

t = get('https://www3.wipo.int/ipstats/main.649b62b91ba3b94e.js', timeout=(10, 120)).text
t2 = get('https://www3.wipo.int/ipstats/184.4739a4f1ffa3d285.js', timeout=(10, 120)).text

# Find _buildHttpParams in 184
for name, txt in [('184', t2)]:
    i = txt.find('_buildHttpParams')
    print(f"=== {name} _buildHttpParams ===")
    print(repr(txt[i:i + 900]))
    print()

# Find the param-name enum (c.B / B.selectedTab etc.) in main
for kw in ['selectedTab', 'fromYear', 'offSelValues', 'oriSelValues', 'classSelValues', 'techSelValues']:
    i = t.find(kw + ':')
    if i == -1:
        i = t.find(kw)
    if i != -1:
        print(f"--- main {kw}: {repr(t[max(0,i-60):i+80])}")

# Find the enum object B={...} that defines param keys
m = re.search(r'selectedTab\s*[:=]\s*"[^"]+"', t)
if m:
    j = m.start()
    print("\n=== param enum block (main) ===")
    print(repr(t[max(0, j - 200):j + 600]))
