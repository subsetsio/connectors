import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re
import lxml.html
from subsets_utils import get

ENTRY = "http://www.moe.gov.cn/jyb_sjzl/moe_560/2024/"


def fetch(url):
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text


def parse_year_index(html, base):
    doc = lxml.html.fromstring(html)
    doc.make_links_absolute(base)
    out = {}
    for a in doc.xpath("//a[@href]"):
        txt = (a.text_content() or "").strip()
        m = re.match(r"^((?:19|20)\d{2})年教育统计数据$", txt)
        if m:
            out.setdefault(int(m.group(1)), a.get("href"))
    return out


def find_quanguo(landing_html, base):
    doc = lxml.html.fromstring(landing_html)
    doc.make_links_absolute(base)
    cands = []
    for a in doc.xpath("//a[@href]"):
        href = a.get("href")
        txt = (a.text_content() or "").strip()
        if "quanguo" in href or "全国" in txt:
            cands.append((txt, href))
    return cands


def list_tables(index_html, base):
    doc = lxml.html.fromstring(index_html)
    doc.make_links_absolute(base)
    out = []
    for a in doc.xpath("//a[@href]"):
        title = (a.get("title") or "").strip()
        href = a.get("href")
        if title and re.search(r"/t\d{8}_\d+\.html$", href):
            out.append((title, href))
    return out


years = parse_year_index(fetch(ENTRY), ENTRY)
print("YEARS:", sorted(years)[:5], "...", sorted(years)[-5:], "count", len(years))

for y in (2023, 2015, 2010):
    if y not in years:
        print(y, "NOT IN INDEX")
        continue
    landing = years[y]
    print(f"\n=== {y} landing {landing} ===")
    try:
        lh = fetch(landing)
    except Exception as e:
        print("  landing fetch failed", e)
        continue
    qg = find_quanguo(lh, landing)
    print("  quanguo candidates:", qg[:4])
    if qg:
        qurl = qg[0][1]
        try:
            ih = fetch(qurl)
            tbls = list_tables(ih, qurl)
            print(f"  index {qurl}: {len(tbls)} table links; sample:", [t[0] for t in tbls[:3]])
        except Exception as e:
            print("  quanguo index fetch failed", e)
