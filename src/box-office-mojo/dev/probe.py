import io
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
    try:
        tables = pd.read_html(io.StringIO(html))
        print("num tables:", len(tables))
        for i, t in enumerate(tables):
            print(f"-- table {i} shape={t.shape}")
            print("   columns:", list(t.columns))
            print(t.head(2).to_string().replace("\n", "\n   "))
    except Exception as e:
        print("read_html err:", type(e).__name__, e)
    return html

h = show("https://www.boxofficemojo.com/year/", "YEAR INDEX")
yrs = sorted(set(re.findall(r'/year/(\d{4})/', h)))
print("year links:", len(yrs), yrs[:2], yrs[-2:] if yrs else "")

show("https://www.boxofficemojo.com/year/2023/", "DOMESTIC YEARLY 2023")

hw = show("https://www.boxofficemojo.com/year/world/", "WORLD YEAR INDEX")
wyrs = sorted(set(re.findall(r'/year/world/(\d{4})/', hw)))
print("world year links:", len(wyrs), wyrs[:2], wyrs[-2:] if wyrs else "")
show("https://www.boxofficemojo.com/year/world/2023/", "WORLDWIDE YEARLY 2023")
