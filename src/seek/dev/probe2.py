import re
from subsets_utils import get, configure_http
configure_http(headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
html = get("https://au.seek.com/about/news/seek-employment-data", timeout=(10,120)).text

for label in ["Download the latest SEEK Employment data", "Download the latest SEEK Advertised Salary"]:
    i = html.find(label)
    print("====", label, "found@", i)
    if i>=0:
        # search backwards for nearest href before the label
        seg = html[max(0,i-400):i+len(label)+50]
        hrefs = re.findall(r'href="(https://[^"]*graphassets\.com/[^"]+)"', seg)
        print("   nearby hrefs:", hrefs)
