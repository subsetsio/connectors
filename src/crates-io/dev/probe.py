"""Probe: stream the crates.io dump tar far enough to read schema.sql +
metadata.json (which precede data/*.csv), then stop. Avoids full download."""
import tarfile
import httpx


class _IterReader:
    """Adapt an httpx byte-iterator to a read()-able stream for tarfile r|gz."""
    def __init__(self, it):
        self._it = it
        self._buf = b""

    def read(self, n=-1):
        if n is None or n < 0:
            chunks = [self._buf]
            self._buf = b""
            chunks.extend(self._it)
            return b"".join(chunks)
        while len(self._buf) < n:
            try:
                self._buf += next(self._it)
            except StopIteration:
                break
        out, self._buf = self._buf[:n], self._buf[n:]
        return out


URL = "https://static.crates.io/db-dump.tar.gz"
WANT = ("schema.sql", "metadata.json")
with httpx.stream("GET", URL, follow_redirects=True, timeout=120.0) as r:
    r.raise_for_status()
    reader = _IterReader(r.iter_bytes(chunk_size=1 << 16))
    tar = tarfile.open(fileobj=reader, mode="r|gz")
    for m in tar:
        base = m.name.rsplit("/", 1)[-1]
        if "/data/" in m.name:
            print("FIRST DATA MEMBER:", m.name)
            break
        if base in WANT:
            data = tar.extractfile(m).read().decode("utf-8", "replace")
            print("=" * 30, base, "=" * 30)
            print(data)
