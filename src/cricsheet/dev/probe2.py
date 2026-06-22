import io, csv, re, collections
from subsets_utils import get
r = get("https://cricsheet.org/register/people.csv", timeout=(10,120)); r.raise_for_status()
rows = list(csv.DictReader(io.StringIO(r.content.decode("utf-8"))))
ids = [x["identifier"] for x in rows]
print("people rows:", len(rows))
print("unique identifiers:", len(set(ids)))
print("hex-id matches:", sum(bool(re.fullmatch(r'[0-9a-f]+', i)) for i in ids), "of", len(ids))
print("cols:", list(rows[0].keys())[:6], "...")
print("empty names:", sum(1 for x in rows if not x.get("name")))
