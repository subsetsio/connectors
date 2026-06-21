import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from subsets_utils import get
for page in ["https://globalcarbonbudget.org/datahub/"]:
    html = get(page, timeout=(10,60)).text
    print("=== ",page, "len", len(html))
    for m in re.finditer(r'href="([^"]*latest-gcb-data[^"]*)"', html, re.I):
        print("  latest-link:", m.group(1))
    # any download links here?
    for m in re.finditer(r'href="(https://globalcarbonbudget\.org/download/\d+/[^"]*)"[^>]*>(.*?)</a>', html, re.S|re.I):
        txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",m.group(2))).strip()
        print("  dl:", repr(txt[:60]),"|",m.group(1))
