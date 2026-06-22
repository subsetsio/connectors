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
        t = tables[0]
        print("shape:", t.shape, "columns:", list(t.columns))
        print(t.head(3).to_string())
    except Exception as e:
        print("read_html err:", type(e).__name__, e)
    return html

# weekend index (per year via ?yr=)
hw = show("https://www.boxofficemojo.com/weekend/?yr=2023", "WEEKEND INDEX 2023")
print("weekend detail links:", sorted(set(re.findall(r'/weekend/(\d{4}W\d{2})/', hw)))[:5])

# weekend detail
show("https://www.boxofficemojo.com/weekend/2023W26/", "WEEKEND DETAIL 2023W26")

# daily index per year
hd = show("https://www.boxofficemojo.com/daily/?yr=2023", "DAILY INDEX 2023")
print("daily date links:", sorted(set(re.findall(r'/date/(\d{4}-\d{2}-\d{2})/', hd)))[:5])
show("https://www.boxofficemojo.com/daily/", "DAILY DEFAULT")

# top lifetime gross + pagination via offset
hc = show("https://www.boxofficemojo.com/chart/top_lifetime_gross/", "TOP LIFETIME GROSS")
print("offset links:", sorted(set(re.findall(r'offset=(\d+)', hc)))[:10])
