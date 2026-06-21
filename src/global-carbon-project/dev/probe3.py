import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from subsets_utils import get
page="https://globalcarbonbudget.org/data-hub/the-latest-gcb-data-2025/"
html = get(page, timeout=(10,60)).text
print("len", len(html))
for m in re.finditer(r'<a[^>]+href="(https://globalcarbonbudget\.org/download/\d+/[^"]*)"[^>]*>(.*?)</a>', html, re.S|re.I):
    txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",m.group(2))).strip()
    print(repr(txt[:70]),"|",m.group(1))
