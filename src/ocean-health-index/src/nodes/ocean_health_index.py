"""Ocean Health Index (OHI) — global assessment scores.

Single-entity, stateless full re-pull. The entire publishable corpus is one
tidy bulk CSV (https://oceanhealthindex.org/data/scores.csv, ~19 MB): one row
per (scenario, goal, dimension, region). The source re-publishes once per
annual assessment cycle and exposes no incremental/delta filter, so we re-fetch
the whole file every run and overwrite — revisions and back-corrections are
picked up for free. The server is slow (~100 KB/s observed), hence the long
read timeout.

Columns (stable headers, no published schema):
  scenario     assessment year (2012-2025)
  goal         goal/sub-goal code (19 incl. composite 'Index')
  long_goal    human label for the goal
  dimension    score | status | trend | future | pressures | resilience
  region_id    OHI region id (0 = 'Global average', 1..220 EEZs/territories)
  region_name  region label
  value        0-100 index value (may be blank/NA -> null)
"""

import csv
import io

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

SCORES_URL = "https://oceanhealthindex.org/data/scores.csv"

SCHEMA = pa.schema(
    [
        ("scenario", pa.int32()),
        ("goal", pa.string()),
        ("long_goal", pa.string()),
        ("dimension", pa.string()),
        ("region_id", pa.int32()),
        ("region_name", pa.string()),
        ("value", pa.float64()),
    ]
)


@transient_retry()
def _download_csv(url: str) -> bytes:
    # Long read timeout: the origin trickles the ~19 MB file at ~100 KB/s.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _to_int(v):
    v = (v or "").strip()
    return int(v) if v not in ("", "NA") else None


def _to_float(v):
    v = (v or "").strip()
    if v in ("", "NA"):
        return None
    return float(v)


def fetch_scores(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    raw = _download_csv(SCORES_URL)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace")))

    cols = {k: [] for k in SCHEMA.names}
    for r in reader:
        cols["scenario"].append(_to_int(r.get("scenario")))
        cols["goal"].append((r.get("goal") or "").strip() or None)
        cols["long_goal"].append((r.get("long_goal") or "").strip() or None)
        cols["dimension"].append((r.get("dimension") or "").strip() or None)
        cols["region_id"].append(_to_int(r.get("region_id")))
        cols["region_name"].append((r.get("region_name") or "").strip() or None)
        cols["value"].append(_to_float(r.get("value")))

    table = pa.table(cols, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ocean-health-index-scores", fn=fetch_scores, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ocean-health-index-scores-transform",
        deps=["ocean-health-index-scores"],
        sql='''
            SELECT
                scenario AS year,
                goal,
                long_goal,
                dimension,
                region_id,
                region_name,
                CAST(value AS DOUBLE) AS value
            FROM "ocean-health-index-scores"
            WHERE value IS NOT NULL
        ''',
    ),
]
