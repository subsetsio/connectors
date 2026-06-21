import io, json, tarfile
from subsets_utils import get_client

URL = "https://github.com/github/advisory-database/archive/refs/heads/main.tar.gz"


class _Reader(io.RawIOBase):
    """Adapt httpx streaming iter_bytes() into a readable file object."""
    def __init__(self, it):
        self._it = it
        self._buf = b""

    def readable(self):
        return True

    def readinto(self, b):
        while not self._buf:
            try:
                self._buf = next(self._it)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


seen = 0
dirs = {}
samples = []
with get_client().stream("GET", URL, timeout=(10.0, 600.0)) as resp:
    resp.raise_for_status()
    print("status", resp.status_code, "ctype", resp.headers.get("content-type"))
    raw = _Reader(resp.iter_bytes())
    tar = tarfile.open(fileobj=raw, mode="r|gz")
    for m in tar:
        if not m.isfile() or not m.name.endswith(".json"):
            continue
        parts = m.name.split("/")
        # parts[0] = github-advisory-database-<sha>
        if len(parts) > 2 and parts[1] == "advisories":
            top = parts[2]
            dirs[top] = dirs.get(top, 0) + 1
        seen += 1
        if len(samples) < 3 and "advisories/" in m.name:
            data = json.loads(tar.extractfile(m).read())
            samples.append((m.name, data))
        if seen >= 4000:
            break

print("json files seen (first batch):", seen)
print("advisories/ subdirs:", dirs)
for name, d in samples:
    print("\n===", name)
    print("top keys:", sorted(d.keys()))
    print("id:", d.get("id"), "| published:", d.get("published"), "| modified:", d.get("modified"))
    print("aliases:", d.get("aliases"))
    print("summary:", (d.get("summary") or "")[:80])
    print("severity:", d.get("severity"))
    print("database_specific:", json.dumps(d.get("database_specific", {}))[:400])
    aff = d.get("affected", [])
    print("affected count:", len(aff))
    if aff:
        print("affected[0]:", json.dumps(aff[0])[:500])
