"""IRS Corporation Source Book (corp-source-book).

Wide zipped-CSV extract probed latest-first at <yy>sb{flt,flat}file.zip; publishes
source-book file 1 (the primary balance-sheet / income detail cross-tabbed by
industry and asset-size class). The most recent year defines the inferred
per-column type schema; every other year is conformed to it.
"""

from __future__ import annotations

from utils import (
    BASE,
    _classify_wide,
    _extract_member,
    _fetch,
    _header_cols,
    _two_digit_years,
    _wide_rows,
    _wide_schema,
    _write_batch,
)

import pyarrow as pa  # noqa: F401  (kept for parity; schema built in utils)


def fetch_corp_source_book(node_id: str) -> None:
    asset = node_id
    typed: list[tuple[str, bool]] | None = None
    schema: pa.Schema | None = None
    found = 0
    for year in sorted(_two_digit_years(2004), reverse=True):
        yy = f"{year % 100:02d}"
        zip_bytes = _fetch(f"{BASE}/{yy}sbfltfile.zip")
        if zip_bytes is None:
            zip_bytes = _fetch(f"{BASE}/{yy}sbflatfile.zip")
        if zip_bytes is None:
            continue
        # Publish source-book file 1 (the primary balance-sheet / income detail
        # cross-tabbed by industry and asset-size class).
        csv_bytes = _extract_member(zip_bytes, needle="sb1")
        if schema is None:
            typed = _classify_wide(csv_bytes, _header_cols(csv_bytes))
            schema = _wide_schema(typed)
        _write_batch(f"{asset}-{year}", schema, _wide_rows(csv_bytes, typed, year))
        found += 1
    if not found:
        raise RuntimeError(f"{asset}: discovered no Corporation Source Book zips under {BASE}")

