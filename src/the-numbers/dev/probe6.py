import re
import lxml.html
from subsets_utils import get

for kind, slug in [("daily","daily-box-office-chart"),
                   ("weekend","weekend-box-office-chart"),
                   ("weekly","weekly-box-office-chart")]:
    url = f"https://www.the-numbers.com/{slug}"
    r = get(url, timeout=(10.0, 60.0))
    doc = lxml.html.fromstring(r.text)
    canon = doc.xpath("//link[@rel='canonical']/@href")
    h1 = [h.text_content().strip() for h in doc.xpath("//h1|//h2")][:3]
    pat = re.compile(rf"/box-office-chart/{kind}/\d{{4}}/\d{{2}}/\d{{2}}")
    dates = sorted(set(pat.search(h).group(0) for a in doc.xpath("//a/@href")
                       for h in [a] if pat.search(h)))
    print(kind, "canonical:", canon)
    print("   h1/h2:", h1)
    print("   date links:", dates)
    # prev/next test from a known dated page: distinguish by comparison
print("---- prev/next on dated daily page ----")
r = get("https://www.the-numbers.com/box-office-chart/daily/2026/06/19", timeout=(10.0,60.0))
doc = lxml.html.fromstring(r.text)
pat = re.compile(r"/box-office-chart/daily/(\d{4})/(\d{2})/(\d{2})")
links = sorted(set(m.group(0) for a in doc.xpath("//a/@href") for m in [pat.search(a)] if m))
print("daily 2026/06/19 date links:", links)
