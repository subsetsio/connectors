"""StatCounter screen-resolution statistic.

`screen-resolution` is special: StatCounter serves it only as an aggregate
(category -> share for a period), not a per-date series. We reconstruct a yearly
series by requesting one aggregate per (region, year), and limit it to worldwide
+ continents to keep the (region x year) fan-out bounded (it is the
lowest-priority subset).
"""

import csv as _csv
import io as _io
import time
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import (
    BASE_URL,
    SOURCE_MIN_YEAR,
    _discover_regions,
    _get_text,
)

# Platform settings under which the statistic is meaningful.
_CFG = {"code": "resolution", "device": "desktop+tablet+mobile", "multi": True}

_RESOLUTION_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("region_code", pa.string()),
    ("region_name", pa.string()),
    ("region_type", pa.string()),
    ("resolution", pa.string()),
    ("market_share", pa.float64()),
])


def _parse_resolution_csv(text: str) -> list[tuple[str, float]]:
    """Aggregate CSV ['Screen Resolution','Market Share Perc. (...)'] -> long
    [(resolution, market_share), ...]."""
    rows = list(_csv.reader(_io.StringIO(text)))
    if len(rows) < 2:
        return []
    out: list[tuple[str, float]] = []
    for r in rows[1:]:
        if len(r) < 2:
            continue
        res = r[0].strip()
        raw = r[1].strip()
        if not res or raw == "":
            continue
        try:
            val = float(raw)
        except ValueError:
            continue
        out.append((res, val))
    return out


def fetch_resolution(node_id: str) -> None:
    """Screen resolution: aggregate-only at source, so fetch one aggregate per
    (region, year) to reconstruct a yearly series. Scoped to worldwide +
    continents to bound the (region x year) fan-out (lowest-priority subset)."""
    asset = node_id
    code, device, multi = _CFG["code"], _CFG["device"], _CFG["multi"]

    regions = [r for r in _discover_regions() if r[2] in ("worldwide", "continent")]
    current_year = datetime.now(tz=timezone.utc).year
    years = list(range(SOURCE_MIN_YEAR, current_year + 1))

    failed = 0
    attempts = 0
    total_rows = 0

    with raw_parquet_writer(asset, _RESOLUTION_SCHEMA) as writer:
        for region_code, region_name, region_type in regions:
            for year in years:
                attempts += 1
                params = {
                    "statType_hidden": code,
                    "region_hidden": region_code,
                    "granularity": "yearly",
                    "csv": "1",
                    "device_hidden": device,
                    "multi-device": "true" if multi else "false",
                    "fromYear": str(year),
                    "toYear": str(year),
                }
                try:
                    text = _get_text(BASE_URL, params)
                except Exception as exc:  # noqa: BLE001
                    print(f"  {asset}: {region_code}/{year} fetch failed: {type(exc).__name__}: {exc}")
                    failed += 1
                    continue

                pairs = _parse_resolution_csv(text)
                if not pairs:
                    continue
                batch = {
                    "year": [year] * len(pairs),
                    "region_code": [region_code] * len(pairs),
                    "region_name": [region_name] * len(pairs),
                    "region_type": [region_type] * len(pairs),
                    "resolution": [res for res, _ in pairs],
                    "market_share": [v for _, v in pairs],
                }
                writer.write_table(pa.table(batch, schema=_RESOLUTION_SCHEMA))
                total_rows += len(pairs)
                time.sleep(0.2)

        if failed > attempts * 0.25:
            raise RuntimeError(f"{asset}: {failed}/{attempts} (region,year) fetches failed (>25%); aborting")
        if total_rows == 0:
            raise RuntimeError(f"{asset}: produced 0 rows; source format likely changed")

    print(f"  {asset}: {total_rows} rows across {len(regions)} regions x {len(years)} years")


DOWNLOAD_SPECS = [
    NodeSpec(id="statcounter-screen-resolution", fn=fetch_resolution, kind="download"),
]


_RESOLUTION_SQL = '''
    SELECT
        make_date(year, 1, 1)         AS year_start,
        year,
        region_code,
        region_name,
        region_type,
        resolution,
        CAST(market_share AS DOUBLE)  AS market_share
    FROM "statcounter-screen-resolution"
    WHERE market_share IS NOT NULL
    QUALIFY row_number() OVER (
        PARTITION BY year, region_code, resolution ORDER BY market_share DESC
    ) = 1
'''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="statcounter-screen-resolution-transform",
        deps=["statcounter-screen-resolution"],
        sql=_RESOLUTION_SQL,
    ),
]
