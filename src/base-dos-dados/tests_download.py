"""Health invariants for the Base dos Dados raw assets.

Each raw asset is a gzipped CSV saved verbatim from the public one-click bucket.
These catch silent degradation that file-existence alone misses: truncated or
empty payloads, a non-gzip body (an HTML error page served as 200), or a CSV
with a header but no data rows.
"""

import gzip

from subsets_utils import load_raw_file


def _decompress(sid):
    raw = load_raw_file(sid, extension="csv.gz", binary=True)
    assert raw and len(raw) > 0, f"{sid}: raw csv.gz is empty"
    assert raw[:2] == b"\x1f\x8b", f"{sid}: not gzip (first bytes {raw[:8]!r})"
    return gzip.decompress(raw)


def test_raw_assets_are_nonempty_csv(spec_ids):
    """Every asset must gunzip to a CSV with a header and at least one data row."""
    for sid in spec_ids:
        text = _decompress(sid)
        lines = text.splitlines()
        assert len(lines) >= 2, (
            f"{sid}: csv has {len(lines)} line(s); expected header + >=1 row"
        )
        assert b"," in lines[0] or b";" in lines[0] or b"\t" in lines[0], (
            f"{sid}: header has no delimiter — {lines[0][:120]!r}"
        )
