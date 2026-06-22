import re
import pandas as pd
from subsets_utils import get

def fetch(url):
    r = get(url, timeout=(10.0, 60.0))
    r.raise_for_status()
    return r.text

def show(url, label):
    print("=" * 70)
    print(label, url)
    html = fetch(url)
    print("len html:", len(html))
    # find year links
    try:
        tables = pd.read_html(html)
        print("num tables:", len(tables))
        t = tables[0]
        print("shape:", t.shape)
        print("columns:", list(t.columns))
        print(t.head(3).to_string())
    except Exception as e:
        print("read_html err:", type(e).__name__, e)
    return html

# 1. year index
h = show("https://www.boxofficemojo.com/year/", "YEAR INDEX")
yrs = sorted(set(re.findall(r'/year/(\d{4})/', h)))
print("year links found:", len(yrs), yrs[:3], yrs[-3:] if yrs else "")

# 2. domestic yearly detail
show("https://www.boxofficemojo.com/year/2023/", "DOMESTIC YEARLY 2023")

# 3. worldwide index + detail
hw = show("https://www.boxofficemojo.com/year/world/", "WORLD YEAR INDEX")
wyrs = sorted(set(re.findall(r'/year/world/(\d{4})/', hw)))
print("world year links:", len(wyrs), wyrs[:3], wyrs[-3:] if wyrs else "")
show("https://www.boxofficemojo.com/year/world/2023/", "WORLDWIDE YEARLY 2023")
