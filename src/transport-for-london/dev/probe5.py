import sys, os, io, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import urllib.parse
keys = """usage-stats/411JourneyDataExtract01Jan2025-14Jan2025.csv
usage-stats/412JourneyDataExtract15Jan2025-31Jan2025.csv
usage-stats/413JourneyDataExtract01Feb2025-14Feb2025.csv""".strip().splitlines()
for key in keys[:1]:
    url = "https://cycling.data.tfl.gov.uk/" + urllib.parse.quote(key.strip(), safe="/")
    r = get(url, timeout=(10,120)); r.raise_for_status()
    txt = r.content[:2000].decode("utf-8","replace")
    rows = list(csv.reader(io.StringIO(txt)))
    print("KEY", key)
    print("HEADER:", rows[0])
    print("ROW1:", rows[1] if len(rows)>1 else None)
