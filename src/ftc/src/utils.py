"""Shared HTTP + CSV helpers for the FTC connector node files.

FTC CSVs embed cp1252 bytes (0x96 en-dash) in free-text industry labels that
break strict UTF-8, so every CSV is decoded as cp1252 and re-emitted as NDJSON
(all values as strings) for the SQL transforms to re-type.
"""

import csv
import io

from subsets_utils import get, transient_retry

BASE = "https://www.ftc.gov"


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _full_url(href: str) -> str:
    return href if href.startswith("http") else BASE + href


def _parse_csv(raw: bytes) -> list[dict]:
    """Decode cp1252 (fixes the 0x96 en-dash) and parse to a list of dicts with
    all-string values, trimming whitespace and dropping any unnamed overflow
    column csv emits for ragged rows."""
    text = raw.decode("cp1252", errors="replace")
    rows = []
    for rec in csv.DictReader(io.StringIO(text)):
        clean = {}
        for k, v in rec.items():
            if k is None:
                continue
            clean[k.strip()] = v.strip() if isinstance(v, str) else v
        rows.append(clean)
    return rows
