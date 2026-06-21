"""NOAA IBTrACS — single global "ALL" best-track CSV (row 2 is a units row,
skipped). IBTrACS global tropical-cyclone best tracks.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer

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


DOWNLOAD_SPECS = [
    NodeSpec(
        id="noaa-international-best-track-archive-for-climate-stewardship-ibtracs",
        fn=fetch_ibtracs,
        kind="download",
    ),
]

_SQL = '''
        SELECT
            SID                                    AS sid,
            TRY_CAST(SEASON AS INT)                AS season,
            TRY_CAST(NUMBER AS INT)                AS storm_number,
            BASIN                                  AS basin,
            SUBBASIN                               AS subbasin,
            NAME                                   AS name,
            TRY_CAST(ISO_TIME AS TIMESTAMP)        AS iso_time,
            NATURE                                 AS nature,
            TRY_CAST(LAT AS DOUBLE)                AS lat,
            TRY_CAST(LON AS DOUBLE)                AS lon,
            TRY_CAST(WMO_WIND AS INT)              AS wmo_wind,
            TRY_CAST(WMO_PRES AS INT)              AS wmo_pres,
            TRY_CAST(DIST2LAND AS INT)             AS dist2land,
            TRY_CAST(LANDFALL AS INT)              AS landfall,
            TRY_CAST(USA_WIND AS INT)              AS usa_wind,
            TRY_CAST(USA_PRES AS INT)              AS usa_pres,
            TRY_CAST(USA_SSHS AS INT)              AS usa_sshs
        FROM "noaa-international-best-track-archive-for-climate-stewardship-ibtracs"
        WHERE TRY_CAST(ISO_TIME AS TIMESTAMP) IS NOT NULL AND SID IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY SID, ISO_TIME ORDER BY SID) = 1
    '''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="noaa-international-best-track-archive-for-climate-stewardship-ibtracs-transform",
        deps=["noaa-international-best-track-archive-for-climate-stewardship-ibtracs"],
        sql=_SQL,
    ),
]
