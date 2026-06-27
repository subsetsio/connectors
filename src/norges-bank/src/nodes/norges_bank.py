"""Norges Bank connector — SDMX 2.1 data warehouse (data.norges-bank.no).

One published table per SDMX dataflow. Each dataflow's full corpus is fetched
in a single request via the 'all' key (`/api/data/{dataflow}/all?format=csv`),
which returns a denormalized long-format CSV: one row per (series-key,
TIME_PERIOD) with an OBS_VALUE. The CSV carries each SDMX component twice — an
uppercase component-id column (e.g. BASE_CUR) and a human-label column (e.g.
"Base Currency"). We keep only the component-id columns plus TIME_PERIOD and
OBS_VALUE, which yields a clean, self-describing schema per dataflow.

Fetch shape: stateless full re-pull. The whole source is small-to-moderate
(most dataflows are a few MB; MONEY_MARKET is ~120MB), the API has no rate
limit, and re-pulling each refresh picks up revisions for free. No watermark,
no cursor. We stream the CSV straight into a gzipped NDJSON raw asset so the
large dataflows never materialize as a giant in-memory row list.

Raw format is NDJSON (not parquet): the column set differs across the 18
dataflows (each has its own DSD), so a single generic fetch fn can't declare
one parquet schema. NDJSON defers typing to the transform, which casts
OBS_VALUE to DOUBLE and leaves the dimension/attribute columns as strings.
TIME_PERIOD is kept as a string because its grain varies by dataflow
(daily dates, "2024", "2026-Q1", ISO datetimes).
"""
import csv
import json
import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "norges-bank"
API = "https://data.norges-bank.no/api"

# SDMX component-id columns are UPPERCASE_SNAKE; the paired human-label columns
# ("Base Currency", "Frequency", ...) are mixed-case / spaced and dropped.
_CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _dataflow_for(node_id: str) -> str:
    """norges-bank-govt-keyfigures -> GOVT_KEYFIGURES."""
    suffix = node_id[len(SLUG) + 1:]
    return suffix.upper().replace("-", "_")


@transient_retry()
def _fetch_csv(dataflow: str):
    # MONEY_MARKET's full CSV is ~120MB and slow; allow a long read timeout.
    resp = get(
        f"{API}/data/{dataflow}/all",
        params={"format": "csv"},
        timeout=(10.0, 600.0),
    )
    resp.raise_for_status()
    return resp


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    dataflow = _dataflow_for(node_id)
    resp = _fetch_csv(dataflow)

    # csv.reader over the response line iterator handles quoting without
    # buffering a second full copy of the payload.
    reader = csv.reader(resp.iter_lines(), delimiter=";")
    header = next(reader)

    # Keep component-id columns only, first occurrence wins (REGNET emits a
    # duplicate REGION column — code and label share the same header text).
    keep_idx: list[int] = []
    cols: list[str] = []
    seen: set[str] = set()
    for i, h in enumerate(header):
        if _CODE_RE.match(h) and h not in seen:
            seen.add(h)
            keep_idx.append(i)
            cols.append(h)

    if "TIME_PERIOD" not in cols or "OBS_VALUE" not in cols:
        raise AssertionError(
            f"{asset}: expected TIME_PERIOD and OBS_VALUE in CSV header, got {cols}"
        )

    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in reader:
            if not row:
                continue
            rec = {
                col: (row[idx] if idx < len(row) else None)
                for col, idx in zip(cols, keep_idx)
            }
            f.write(json.dumps(rec, separators=(",", ":")))
            f.write("\n")
            n += 1

    if n == 0:
        raise AssertionError(f"{asset}: parsed 0 observations from {dataflow}")
    print(f"  {asset}: {n:,} observations")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One Delta table per dataflow. Thin parse pass: cast OBS_VALUE to DOUBLE,
# drop non-finite / unparseable observations (FAUCTION carries 'NaN' and empty
# OBS_VALUE on announcement rows). All other columns pass through as the SDMX
# component codes (strings); UNIT_MULT/DECIMALS are retained so consumers can
# scale OBS_VALUE themselves.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (TRY_CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
            FROM "{s.id}"
            WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
              AND isfinite(TRY_CAST(OBS_VALUE AS DOUBLE))
        ''',
    )
    for s in DOWNLOAD_SPECS
]
