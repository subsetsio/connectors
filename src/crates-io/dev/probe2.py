"""Sample the first few rows of early CSV members to confirm delimiter,
boolean repr, and timestamp format."""
import tarfile
import httpx


class _IterReader:
    def __init__(self, it):
        self._it = it
        self._buf = b""

    def read(self, n=-1):
        if n is None or n < 0:
            chunks = [self._buf]; self._buf = b""; chunks.extend(self._it)
            return b"".join(chunks)
        while len(self._buf) < n:
            try:
                self._buf += next(self._it)
            except StopIteration:
                break
        out, self._buf = self._buf[:n], self._buf[n:]
        return out


URL = "https://static.crates.io/db-dump.tar.gz"
WANT = {"categories.csv", "crate_downloads.csv", "crates.csv", "crates_categories.csv"}
got = set()
with httpx.stream("GET", URL, follow_redirects=True, timeout=120.0) as r:
    r.raise_for_status()
    tar = tarfile.open(fileobj=_IterReader(r.iter_bytes(chunk_size=1 << 16)), mode="r|gz")
    for m in tar:
        base = m.name.rsplit("/", 1)[-1]
        if "/data/" in m.name and base in WANT:
            f = tar.extractfile(m)
            head = f.read(2000).decode("utf-8", "replace").splitlines()[:4]
            print("=" * 20, base, "=" * 20)
            for line in head:
                print(line[:400])
            got.add(base)
            if got == WANT:
                break
