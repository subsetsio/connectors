import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from lxml import html as lh
import re
url = "https://www.pordata.pt/en/europe/resident+population-1951"
r = get(url, timeout=(10,60))
h = r.text
doc = lh.fromstring(h)
forms = doc.xpath("//form")
print("forms:", len(forms))
for fm in forms:
    print("  action=", fm.get("action"), "method=", fm.get("method"), "id=", fm.get("id"))
# hidden inputs
hidden = doc.xpath("//input[@type='hidden']")
print("hidden inputs:", len(hidden))
for i in hidden[:25]:
    v = (i.get("value") or "")[:30]
    print("   ", i.get("name"), "=", v)
# look for table/tabela toggle text & ValueCell presence
print("ValueCell in initial GET:", h.count("ValueCell"))
print("indicator-data in initial:", h.count("indicator-data"))
for kw in ["Table","Tabela","Grelha","grid","View Ranking","Chart"]:
    print(f"  '{kw}':", h.count(kw))
# OutSystems version / module
m = re.findall(r'OsName["\']?\s*[:=]\s*["\']([^"\']+)', h)
print("OsName:", m[:3])
