import gzip, io, json, tarfile, tempfile, os
import duckdb
from subsets_utils import get_client
import nodes.github as g

URL = g.ARCHIVE_URL


class _Reader(io.RawIOBase):
    def __init__(self, it):
        self._it = it; self._buf = b""
    def readable(self): return True
    def readinto(self, b):
        while not self._buf:
            try: self._buf = next(self._it)
            except StopIteration: return 0
        n = min(len(b), len(self._buf)); b[:n] = self._buf[:n]; self._buf = self._buf[n:]; return n

adv, aff = [], []
with get_client().stream("GET", URL, timeout=(10.0, 600.0)) as resp:
    resp.raise_for_status()
    tar = tarfile.open(fileobj=_Reader(resp.iter_bytes()), mode="r|gz")
    for m in tar:
        if not m.isfile() or not m.name.endswith(".json"): continue
        parts = m.name.split("/")
        if len(parts) < 4 or parts[1] != "advisories": continue
        sd = parts[2]
        d = json.loads(tar.extractfile(m).read())
        if not d.get("id"): continue
        adv.append(g._advisory_row(sd, d))
        aff.extend(g._affected_rows(sd, d))
        if len(adv) >= 3000: break

d = tempfile.mkdtemp()
ap = os.path.join(d, "adv.ndjson.gz"); fp = os.path.join(d, "aff.ndjson.gz")
with gzip.open(ap, "wt") as f:
    for r in adv: f.write(json.dumps(r) + "\n")
with gzip.open(fp, "wt") as f:
    for r in aff: f.write(json.dumps(r) + "\n")

print("parsed advisories:", len(adv), "affected:", len(aff))
print("sample advisory:", json.dumps(adv[0]))
print("sample affected:", json.dumps(aff[0]) if aff else None)

adv_sql = g.TRANSFORM_SPECS[0].sql.replace('"github-advisories"', f"read_json_auto('{ap}')")
aff_sql = g.TRANSFORM_SPECS[1].sql.replace('"github-affected"', f"read_json_auto('{fp}')")

r1 = duckdb.sql(adv_sql)
print("\nADVISORIES transform cols:", r1.columns)
print("dtypes:", r1.types)
print("rows:", duckdb.sql(f"SELECT count(*) FROM ({adv_sql})").fetchone()[0])
print("sample:", duckdb.sql(f"SELECT ghsa_id,severity,published_at,github_reviewed,source_directory FROM ({adv_sql}) LIMIT 3").fetchall())

r2 = duckdb.sql(aff_sql)
print("\nAFFECTED transform cols:", r2.columns)
print("rows:", duckdb.sql(f"SELECT count(*) FROM ({aff_sql})").fetchone()[0])
print("ecosystems:", duckdb.sql(f"SELECT ecosystem, count(*) c FROM ({aff_sql}) GROUP BY 1 ORDER BY 2 DESC LIMIT 8").fetchall())
print("sample:", duckdb.sql(f"SELECT * FROM ({aff_sql}) LIMIT 3").fetchall())
