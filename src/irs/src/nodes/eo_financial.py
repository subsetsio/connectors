"""IRS Exempt Organizations financial extracts (990 / 990EZ / 990PF).

Wide zipped-CSV extracts probed latest-first at <yy>eoextract<form>.zip (one CSV
member). One parametric fetch drives all three forms; the most recent (widest)
year defines the inferred per-column type schema, and every other year is
conformed to it (missing cols -> null, extras dropped).
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

_EO_FORM = {
    "irs-eo-financial-990": "990",
    "irs-eo-financial-990ez": "990EZ",
    "irs-eo-financial-990pf": "990pf",
}


def fetch_eo_financial(node_id: str) -> None:
    asset = node_id
    form = _EO_FORM[node_id]

    # Probe latest-first so the most recent (widest) year defines the schema;
    # infer per-column types from it and conform every other year (missing cols
    # -> null, extras dropped).
    typed: list[tuple[str, bool]] | None = None
    schema: pa.Schema | None = None
    found = 0
    for year in sorted(_two_digit_years(2013), reverse=True):
        yy = f"{year % 100:02d}"
        zip_bytes = _fetch(f"{BASE}/{yy}eoextract{form}.zip")
        if zip_bytes is None:
            continue
        csv_bytes = _extract_member(zip_bytes)
        if schema is None:
            typed = _classify_wide(csv_bytes, _header_cols(csv_bytes))
            schema = _wide_schema(typed)
        _write_batch(f"{asset}-{year}", schema, _wide_rows(csv_bytes, typed, year))
        found += 1
    if not found:
        raise RuntimeError(f"{asset}: discovered no {form} extract zips under {BASE}")

