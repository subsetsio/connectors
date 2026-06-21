import io, time, re
import pandas as pd
import lxml.html as LH
from subsets_utils import get

BASE = "https://www.olympedia.org"

def fetch(path):
    r = get(BASE + path, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.text

def show_tables(path, label):
    print("=" * 70)
    print(label, path)
    html = fetch(path)
    try:
        tables = pd.read_html(io.StringIO(html))
    except Exception as e:
        print("  read_html error:", e)
        tables = []
    print(f"  #tables={len(tables)}")
    for i, t in enumerate(tables):
        print(f"  -- table[{i}] shape={t.shape} cols={list(t.columns)[:10]}")
        print("     head:")
        print(t.head(3).to_string().replace("\n", "\n     "))
    return html

# 1. editions: need edition ids from links
html = show_tables("/editions", "EDITIONS")
doc = LH.fromstring(html)
ed_links = [a.get("href") for a in doc.xpath('//a[contains(@href,"/editions/")]')]
print("  sample edition hrefs:", ed_links[:8], " total:", len(ed_links))
time.sleep(3)

# 4. medals_by_country
show_tables("/statistics/medal/country", "MEDALS_BY_COUNTRY")
time.sleep(3)

# an edition medal table
html = show_tables("/editions/63", "EDITION 63 (Paris 2024)")
doc = LH.fromstring(html)
noc_links = [a.get("href") for a in doc.xpath('//a[contains(@href,"/countries/")]')]
print("  sample country hrefs on edition page:", noc_links[:8])
time.sleep(3)

# 7. records discipline links
html = show_tables("/records", "RECORDS")
doc = LH.fromstring(html)
rec_links = [a.get("href") for a in doc.xpath('//a[contains(@href,"/records/")]')]
print("  sample record hrefs:", rec_links[:12], " total:", len(rec_links))
