import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re, html
from subsets_utils import get
import pandas as pd

INDEX="https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/"
page=get(INDEX, timeout=(10,120)).text
# map table_id -> xls href
hrefs={}
for m in re.finditer(r'href="([^"]+/(\d+\.\d+)\.xlsx?)"', page):
    hrefs.setdefault(m.group(2), m.group(1))

for tid in ["1.1","9.1","3.2","15.1","22.1","14.1"]:
    url=hrefs.get(tid)
    print("="*70)
    print(tid, url)
    if not url: 
        print("  NO HREF"); continue
    r=get(url, timeout=(10,120)); 
    ext = url.rsplit('.',1)[-1]
    try:
        df=pd.read_excel(io.BytesIO(r.content), header=None, engine=('openpyxl' if ext=='xlsx' else 'xlrd'))
    except Exception as e:
        print("  read err",type(e).__name__,e); continue
    print("  shape",df.shape)
    with pd.option_context('display.max_columns',12,'display.width',180):
        print(df.head(12).to_string())
