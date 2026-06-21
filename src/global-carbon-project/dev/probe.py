import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from subsets_utils import get
html = get("https://globalcarbonbudget.org/archive/", timeout=(10,60)).text
print("len", len(html))
for m in re.finditer(r'<a[^>]+href="(https://globalcarbonbudget\.org/download/\d+/[^"]*)"[^>]*>(.*?)</a>', html, re.S|re.I):
    url, txt = m.group(1), re.sub(r"<[^>]+>"," ",m.group(2))
    txt = re.sub(r"\s+"," ",txt).strip()
    print(repr(txt[:75]), "|", url)
