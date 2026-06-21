import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import re
url = "https://www.pordata.pt/en/europe/resident+population-1951"
r = get(url, timeout=(10,60))
h = r.text
# find links/endpoints mentioning table, tbl, db/, screenservices, DataGrid, ambiente
for pat in [r'href="[^"]*tabela[^"]*"', r'https?://tbl\.pordata\.pt[^"\' <]*', r'/db/[^"\' <]*',
            r'screenservices[^"\' ]*', r'DataActionGet\w*', r'"[^"]*GetData[^"]*"',
            r'href="[^"]*[Tt]able[^"]*"']:
    m = re.findall(pat, h)
    print(pat, "->", len(m))
    for x in sorted(set(m))[:6]:
        print("    ", x[:140])
