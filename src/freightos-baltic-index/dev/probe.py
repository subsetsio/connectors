import re, json
from subsets_utils import get

EMBED = "AcDi5xXouXrzQMLqbVpj"
r = get("https://infogram.com/_/" + EMBED, timeout=(10,60))
print("embed status", r.status_code, "len", len(r.text))
m = re.search(r'"key"\s*:\s*"([0-9a-fA-F-]{20,})"\s*,\s*"provider"\s*:\s*"atlas_google_drive"', r.text)
print("key:", m.group(1) if m else None)
key = m.group(1)
r2 = get("https://live-data.jifo.co/" + key, timeout=(10,60))
print("jifo status", r2.status_code, "ct", r2.headers.get("content-type"))
j = r2.json()
print("topkeys", list(j.keys()))
idx = j["sheetNames"].index("FBX Full Data")
grid = j["data"][idx]
print("header", grid[0])
print("rows", len(grid), "first", grid[1], "last", grid[-1])
