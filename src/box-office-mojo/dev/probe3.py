import io
import re
import pandas as pd
from subsets_utils import get

def fetch(url):
    r = get(url, timeout=(10.0, 60.0))
    r.raise_for_status()
    return r.text

# Inspect daily page links / select options for year navigation
h = fetch("https://www.boxofficemojo.com/daily/")
# all hrefs containing 'daily' or 'year' or 'date'
hrefs = sorted(set(re.findall(r'href="([^"]*(?:daily|/year/|byyear|/date/)[^"]*)"', h)))
print("DAILY page candidate nav hrefs (first 25):")
for x in hrefs[:25]:
    print("  ", x)

# try the byyear style
for url in [
    "https://www.boxofficemojo.com/daily/2023/",
    "https://www.boxofficemojo.com/year/2023/?view=releaseDate",
]:
    try:
        t = pd.read_html(io.StringIO(fetch(url)))[0]
        print("OK", url, t.shape, list(t.columns)[:4])
        print("   first Date:", t.iloc[0, 0])
    except Exception as e:
        print("ERR", url, type(e).__name__, str(e)[:80])

# weekend index sanity: confirm yr param filters
hw = fetch("https://www.boxofficemojo.com/weekend/?yr=1995")
tw = pd.read_html(io.StringIO(hw))[0]
print("WEEKEND 1995 first row:", tw.iloc[0].to_dict())
print("weekend 1995 detail ids:", sorted(set(re.findall(r'/weekend/(\d{4}W\d{2})/', hw)))[:3])
