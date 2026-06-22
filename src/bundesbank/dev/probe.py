import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get_client
SDMX_CSV = "application/vnd.sdmx.data+csv;version=1.0.0"
client = get_client()
url = "https://api.statistiken.bundesbank.de/rest/data/BBAPV"
with client.stream("GET", url, headers={"Accept": SDMX_CSV}, timeout=(15.0, 120.0)) as resp:
    print("status", resp.status_code)
    lines = []
    for i, line in enumerate(resp.iter_lines()):
        lines.append(line)
        if i >= 5:
            break
header = lines[0].lstrip("﻿").split(";")
print("NCOLS", len(header))
print("HEADER", header)
for l in lines[1:4]:
    print("ROW", l.split(";"))
