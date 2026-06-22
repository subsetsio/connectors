from subsets_utils import get, configure_http

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

url = "https://w3techs.com/technologies/history_overview/content_management/ms/y"
r = get(url, timeout=(10.0, 120.0))
print("status:", r.status_code)
print("len:", len(r.text))
html = r.text

# Find the data table region
import re
# Print a slice around the first occurrence of a known tech name
for marker in ["WordPress", "history", "<table", "percentages", "data-"]:
    idx = html.find(marker)
    print(f"\n=== marker {marker!r} at {idx} ===")
    if idx >= 0:
        print(html[idx-200:idx+400])
