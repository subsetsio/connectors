"""Shared HTTP + parse helpers for the Netflix Top 10 connector.

Source: the official Netflix Top 10 site. top10.netflix.com 301-redirects to
www.netflix.com/tudum/top10/data/, which serves three fixed-name TSV files, each
the full corpus in one GET (no pagination, no auth).

Fetch shape: stateless full re-pull. Each file is a complete snapshot that grows
by one week every Tuesday, so we re-fetch the whole file every run and overwrite
— no watermark/cursor (there is no incremental query filter, and the files are
small enough to re-pull in seconds). Late corrections are picked up for free.
"""

import csv
import io

from subsets_utils import get, transient_retry

BASE = "https://www.netflix.com/tudum/top10/data"


@transient_retry()
def fetch_tsv(filename: str) -> list:
    """GET one Top 10 TSV and return its rows as a list of dicts. HEAD 403s on
    this host, so always GET."""
    resp = get(f"{BASE}/{filename}", timeout=(10.0, 300.0))
    resp.raise_for_status()
    reader = csv.DictReader(io.StringIO(resp.text), delimiter="\t")
    rows = list(reader)
    if not rows:
        raise AssertionError(f"{filename}: returned 0 data rows")
    return rows


def to_int(v):
    v = (v or "").strip()
    return int(v) if v else None


def to_float(v):
    v = (v or "").strip()
    return float(v) if v else None


def s(v):
    """Normalise a string cell; empty -> None (keeps 'N/A' verbatim for the
    transform to NULLIF)."""
    v = (v or "").strip()
    return v if v else None
