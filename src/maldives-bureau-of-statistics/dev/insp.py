import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re
import pandas as pd
from subsets_utils import get
page=get("https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/", timeout=(10,120)).text
hrefs={}
for m in re.finditer(r'href="([^"]+/(\d+\.\d+)\.xlsx?)"', page):
    hrefs.setdefault(m.group(2), m.group(1))
for tid in ["12.7","24.3"]:
    url=hrefs[tid]; ext=url.rsplit('.',1)[-1]
    r=get(url, timeout=(10,120))
    df=pd.read_excel(io.BytesIO(r.content), header=None, engine=('openpyxl' if ext=='xlsx' else 'xlrd'))
    print("="*60, tid, df.shape, url)
    with pd.option_context('display.max_columns',12,'display.width',200,'display.max_colwidth',40):
        print(df.head(14).to_string())
