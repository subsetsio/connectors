"""Shared NOAA NCEI transport + parse helpers.

Mechanism: ncei_bulk (https://www.ncei.noaa.gov/data/ and /pub/data/). No auth,
no token. Fetch shape: **stateless full re-pull** every refresh — each dataset
here is bounded (tens of thousands to ~1.5M rows) and cheap to re-fetch, and the
source overwrites its bulk files in place (no usable `since`/cursor delta), so a
stored watermark would only risk skipping revised rows. Raw is saved as parquet
with an all-string schema (the source CSVs carry sentinel blanks / mixed types);
the SQL transforms do the typed parse-and-cast.
"""

import re

import pyarrow as pa

from subsets_utils import get, transient_retry

NCEI = "https://www.ncei.noaa.gov"

# --------------------------------------------------------------------------- #
# transport — retry transient (429/5xx/timeouts), surface everything else
# --------------------------------------------------------------------------- #


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_text(url: str, encoding: str | None = None) -> str:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    if encoding:
        resp.encoding = encoding
    return resp.text


def _list_hrefs(url: str) -> list[str]:
    """Apache autoindex links, excluding sort and parent-dir links."""
    html = _get_text(url)
    return [h for h in re.findall(r'href="([^"?][^"]*)"', html) if not h.startswith("..")]


def _clean(v):
    return v if v not in (None, "", " ") else None


def _string_table(header: list[str], rows, schema: pa.Schema) -> tuple[pa.Table, int]:
    """Build the all-string table, DROPPING rows whose field count differs from
    the header. Returns (table, dropped).

    Never pad: a short row means a field vanished mid-line (the RSI export emits
    a handful of 22-field rows with `End` missing), so right-padding shifts every
    later value one column left — `End` silently receives RSI's number. Callers
    bound `dropped`; a jump means the source layout moved.
    """
    cols: dict[str, list] = {c: [] for c in header}
    n = len(header)
    dropped = 0
    for row in rows:
        if len(row) != n:
            dropped += 1
            continue
        for c, v in zip(header, row):
            cols[c].append(_clean(v))
    table = pa.table(
        {c: pa.array(cols[c], type=pa.string()) for c in header}, schema=schema
    )
    return table, dropped


def _normalize_header(header: list[str]) -> list[str]:
    out, seen = [], {}
    for i, c in enumerate(header):
        name = (c or "").strip() or f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out
