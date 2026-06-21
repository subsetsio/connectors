"""JetBrains State of Developer Ecosystem 2025 connector.

The 2025 interactive report (devecosystem-2025.jetbrains.com) renders every
chart from a static per-chart CSV at /_data/<slug>.csv. Each CSV shares one
4-column schema: unit,label,group,value (unit is almost always '%'; label is
the category, e.g. a language/country/option; group splits a category into
sub-series — a survey year for the *_dynamics charts, a stance for delegation,
or the literal 'shares' for single-series charts; value is the percentage).

Each chart is a semantically distinct statistical table, so we emit one
download spec + one transform per chart (the rank-active entity union, 16).

Fetch shape: stateless full re-pull. Files are tiny static CDN assets (<2KB),
re-fetched whole every run and overwritten — no state, no watermark. The
survey is annual and each edition publishes on a new hostname, so there is no
in-place incremental update to track.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

ID_PREFIX = "jetbrains-state-of-developer-ecosystem-"
DATA_BASE = "https://devecosystem-2025.jetbrains.com/_data/"

# Stable contract for the uniform 4-column chart CSV.
SCHEMA = pa.schema([
    ("unit", pa.string()),
    ("label", pa.string()),
    ("group", pa.string()),
    ("value", pa.float64()),
])


def _slug_from_node_id(node_id: str) -> str:
    """Recover the CSV slug from the spec id. Chart slugs use underscores; the
    spec id image converts them to hyphens, so reverse that."""
    return node_id[len(ID_PREFIX):].replace("-", "_")


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id
    slug = _slug_from_node_id(node_id)
    url = f"{DATA_BASE}{slug}.csv"

    text = _fetch_csv(url)
    reader = csv.DictReader(io.StringIO(text))

    units, labels, groups, values = [], [], [], []
    for row in reader:
        raw_val = (row.get("value") or "").strip()
        try:
            val = float(raw_val) if raw_val != "" else None
        except ValueError:
            val = None
        units.append((row.get("unit") or "").strip() or None)
        labels.append((row.get("label") or "").strip() or None)
        groups.append((row.get("group") or "").strip() or None)
        values.append(val)

    if not labels:
        raise AssertionError(f"{asset}: parsed 0 rows from {url}")

    table = pa.table(
        {"unit": units, "label": labels, "group": groups, "value": values},
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{ID_PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per chart. Thin parse/rename/dedup pass:
#   label  -> category   (the option being measured)
#   group  -> series     (sub-series split: survey year, stance, or 'shares')
#   value  -> value      (DOUBLE; the percentage/number)
#   unit   -> unit
# Dedup defensively on (category, series) keeping the last-seen value, and drop
# null values so a malformed cell can't publish a phantom row.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT category, series, unit, value
            FROM (
                SELECT
                    label                  AS category,
                    "group"                AS series,
                    unit                   AS unit,
                    CAST(value AS DOUBLE)  AS value,
                    row_number() OVER (
                        PARTITION BY label, "group"
                        ORDER BY value DESC
                    ) AS rn
                FROM "{s.id}"
                WHERE value IS NOT NULL AND label IS NOT NULL
            )
            WHERE rn = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
