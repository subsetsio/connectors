"""NOAA IBTrACS — single global "ALL" best-track CSV (row 2 is a units row,
skipped). IBTrACS global tropical-cyclone best tracks.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import raw_parquet_writer

from utils import NCEI, _clean, _get_text

IBTRACS_URL = (
    f"{NCEI}/data/international-best-track-archive-for-climate-stewardship-ibtracs/"
    "v04r01/access/csv/ibtracs.ALL.list.v04r01.csv"
)
IBTRACS_KEEP = [
    "SID", "SEASON", "NUMBER", "BASIN", "SUBBASIN", "NAME", "ISO_TIME", "NATURE",
    "LAT", "LON", "WMO_WIND", "WMO_PRES", "DIST2LAND", "LANDFALL",
    "USA_WIND", "USA_PRES", "USA_SSHS",
]


def fetch_ibtracs(node_id: str) -> None:
    asset = node_id
    text = _get_text(IBTRACS_URL)
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    next(reader)  # units row
    idx = {name: header.index(name) for name in IBTRACS_KEEP}  # KeyError-by-design if absent
    schema = pa.schema([(c, pa.string()) for c in IBTRACS_KEEP])

    batch: dict[str, list] = {c: [] for c in IBTRACS_KEEP}
    count = 0

    def _flush(w):
        nonlocal batch
        if batch[IBTRACS_KEEP[0]]:
            w.write_table(
                pa.table(
                    {c: pa.array(batch[c], type=pa.string()) for c in IBTRACS_KEEP},
                    schema=schema,
                )
            )
            batch = {c: [] for c in IBTRACS_KEEP}

    with raw_parquet_writer(asset, schema) as w:
        for row in reader:
            if not row:
                continue
            for c in IBTRACS_KEEP:
                j = idx[c]
                batch[c].append(_clean(row[j]) if j < len(row) else None)
            count += 1
            if count % 200000 == 0:
                _flush(w)
        _flush(w)
    if count < 50000:
        raise RuntimeError(f"ibtracs: only {count} track rows parsed")

