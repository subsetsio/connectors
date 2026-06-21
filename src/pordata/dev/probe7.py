import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import re
url = "https://www.pordata.pt/en/europe/resident+population-1951"
r = get(url, timeout=(10,60))
h = r.text
# contexts around 'Table' that are not part of unrelated words
for m in re.finditer(r'.{50}>Table<.{20}|.{60}Table[ _]?[Vv]iew.{20}|onclick="[^"]*[Tt]able[^"]*"', h):
    print("…", m.group(0)[:130].replace("\n"," "))
print("---- hrefs with db/ or tbl or DataGrid ----")
for m in set(re.findall(r'(?:href|src|action)="([^"]*(?:/db/|tbl\.pordata|DataGrid|Tabela|ConsultEnv|ambiente)[^"]*)"', h)):
    print("  ", m[:140])
print("---- any URL containing the indicator id 1951 ----")
for m in set(re.findall(r'["\'](/[^"\']*1951[^"\']*)["\']', h))[:15]:
    print("  ", m[:140])
