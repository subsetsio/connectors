"""CPI latest-detail — per-country underlying source component scores.

One published subset parsed from the "CPI2025" sheet of the annual TI CPI
workbook: the columns to the right of the Upper CI column are the underlying
source components feeding each country's headline score.
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import build_reader, download_workbook, find_header, col_index, num


def _parse_latest_detail(rows_of) -> list:
    rows = rows_of("CPI2025")
    h = find_header(rows, "Country / Territory")
    hdr = rows[h]
    upper_cols = [c for c, t in hdr.items() if t and "Upper CI" in t]
    assert upper_cols, "no 'Upper CI' column in CPI detail header; layout changed"
    upper_idx = col_index(upper_cols[0])
    # Underlying-source component columns are everything to the right of Upper CI.
    src_cols = {c: hdr[c].strip() for c in hdr if hdr[c] and col_index(c) > upper_idx}
    assert src_cols, "no underlying-source columns found in CPI detail sheet"

    out = []
    for r in rows[h + 1:]:
        country = (r.get("A") or "").strip()
        iso3 = (r.get("B") or "").strip()
        if not country or len(iso3) != 3:
            continue
        region = (r.get("C") or "").strip() or None
        for col, source_name in src_cols.items():
            score = num(r.get(col))
            if score is None:
                continue
            out.append({
                "country": country,
                "iso3": iso3,
                "region": region,
                "source_name": source_name,
                "source_score": score,
            })
    return out


_DETAIL_SCHEMA = pa.schema([
    ("country", pa.string()),
    ("iso3", pa.string()),
    ("region", pa.string()),
    ("source_name", pa.string()),
    ("source_score", pa.float64()),
])


def fetch_latest_detail(node_id: str) -> None:
    rows = _parse_latest_detail(build_reader(download_workbook()))
    assert rows, "CPI latest-detail parsed to 0 rows"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_DETAIL_SCHEMA), node_id)

