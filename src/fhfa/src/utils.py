"""Shared HTTP + CSV->parquet helpers for the FHFA connector.

FHFA exposes no queryable API — every product is a downloadable flat file on
fhfa.gov (chosen mechanism `bulk_files`). All fetches are stateless full
re-pulls: the files are small-to-medium and FHFA publishes revised/restated
history, so we never trust a watermark — re-download in full each refresh and
overwrite.

Raw is written as parquet with every column kept as a STRING (we read CSVs with
explicit all-string types). This preserves leading zeros in FIPS/geo codes and
sidesteps per-column type inference; the per-subset transforms do the casting.

This module holds the code shared across 2+ node files (HTTP client, CSV/zip
parsers, year-discovery). It contains NO NodeSpec definitions.
"""

from __future__ import annotations

import io
import zipfile
from datetime import datetime, timezone

import httpx
import pyarrow as pa

from subsets_utils import get, save_raw_parquet, transient_retry

# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #


@transient_retry()
def _get(url: str) -> httpx.Response:
    """GET with transient-retry. Raises on 4xx/5xx (5xx/429 are retried first)."""
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _get_optional(url: str) -> httpx.Response | None:
    """Like _get but returns None on a 404 (used for year/version discovery)."""
    try:
        return _get(url)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return None
        raise


def _current_year() -> int:
    return datetime.now(timezone.utc).year


# --------------------------------------------------------------------------- #
# CSV -> all-string parquet helpers
# --------------------------------------------------------------------------- #
def _csv_bytes_to_string_table(data: bytes, columns: list[str]) -> pa.Table:
    """Read CSV bytes with every listed column forced to string (preserves
    leading zeros; nulls/empties become null). pyarrow keeps memory bounded for
    the multi-million-row PUDB files."""
    import pyarrow.csv as pacsv

    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in columns})
    table = pacsv.read_csv(io.BytesIO(data), convert_options=convert)
    return table


def _df_to_string_parquet(df: pd.DataFrame, asset: str) -> None:
    """Save a small pandas frame (already all-string) as parquet."""
    import pandas as pd

    df = df.astype("string").where(pd.notna(df), None)
    table = pa.Table.from_pandas(df, preserve_index=False)
    save_raw_parquet(table, asset)


def _unzip_single_csv(content: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(names) != 1:
            raise AssertionError(f"expected exactly one CSV in zip, got {names}")
        return zf.read(names[0])


def _unzip_csvs(content: bytes) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        for n in zf.namelist():
            if n.lower().endswith(".csv"):
                out[n] = zf.read(n)
    if not out:
        raise AssertionError("no CSV members found in zip")
    return out


def _clean_money(v):
    """Strip currency/percent formatting ('$266,036 ' -> '266036',
    '30.00%' -> '30.00') leaving a bare numeric string (or None)."""
    if v is None:
        return None
    s = str(v).replace("$", "").replace(",", "").replace("%", "").strip()
    if not s:
        return None
    try:
        float(s)  # placeholders like '-' / 'N/A' become null
    except ValueError:
        return None
    return s


# --------------------------------------------------------------------------- #
# PUDB enterprise helpers — shared by single-family & multifamily node files
# --------------------------------------------------------------------------- #
def _latest_year_zip(url_tmpl: str) -> bytes:
    for year in range(_current_year() + 2, 2007, -1):
        resp = _get_optional(url_tmpl.format(year=year))
        if resp is not None:
            return resp.content
    raise AssertionError(f"no PUDB release found for any year via {url_tmpl}")


def _pudb_zip_to_parquet(content: bytes, columns: list[str], asset: str) -> None:
    members = _unzip_csvs(content)
    tables = [_csv_bytes_to_string_table(b, columns) for b in members.values()]
    combined = pa.concat_tables(tables)
    save_raw_parquet(combined, asset)


# --------------------------------------------------------------------------- #
# SQL transform helper — shared by the PUDB SF/MF transforms
# --------------------------------------------------------------------------- #
def _int_casts(cols):
    return ",\n            ".join(
        f"CAST(NULLIF({c}, '') AS BIGINT) AS {c}" for c in cols
    )
