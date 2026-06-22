"""CSO Ireland (PxStat) connector.

Each PxStat 'matrix' (table) is one publishable Delta table. The catalog lists
12,708 tables; rank selected 6,341 for publication (see src/constants.py). Each
table is fetched in full from the PxStat RESTful ReadDataset endpoint as flat
CSV — one stable URL per matrix, no pagination, full content per request.

Fetch shape: stateless full re-pull (shape 1). Each table is small (KBs to tens
of MB) and the source exposes no delta filter, so every run re-fetches the whole
table and overwrites. Revisions are picked up for free.

Raw format: NDJSON. The CSV column set differs per matrix (each table has its
own dimensions), so a single shared parquet schema can't cover the corpus;
NDJSON carries each table's own columns without a schema burden, and the
transform re-types VALUE in SQL. Columns common to every table: STATISTIC,
'Statistic Label', UNIT, VALUE, plus that table's dimension code/label columns.
"""

import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_asset_exists,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENTITY_IDS

DATASET_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/{matrix}/CSV/1.0/en"
)

# spec id -> original matrix id. Built once so fetch_one recovers the exact,
# case-preserved matrix from the (lowercased) node id it is handed.
ID_TO_MATRIX = {
    f"central-statistics-office-{eid.lower().replace('_', '-')}": eid
    for eid in ENTITY_IDS
}


@transient_retry()
def _fetch_csv(matrix: str) -> str:
    resp = get(DATASET_URL.format(matrix=matrix), timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    # Idempotent within a run scope: this connector spans 6,341 tables and a
    # single GitHub job (6h cap) cannot fetch them all, so a run finishes across
    # several self-retriggered continuation jobs that share one run_id (and one
    # raw scope). Skipping tables already pulled in this run lets each
    # continuation make fresh progress instead of re-fetching from the top.
    if raw_asset_exists(asset, ext="ndjson.zst"):
        return
    matrix = ID_TO_MATRIX[node_id]
    text = _fetch_csv(matrix)
    # PxStat CSV is UTF-8 with a BOM; strip it so the first header isn't mangled.
    if text and text[0] == "﻿":
        text = text[1:]
    rows = list(csv.DictReader(io.StringIO(text)))
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"central-statistics-office-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per matrix. The CSV column set is dynamic per table,
# so the transform republishes every column (SELECT *) and only re-types the
# always-present VALUE column to DOUBLE (suppressed/blank cells become NULL).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (TRY_CAST("VALUE" AS DOUBLE) AS "VALUE")
            FROM "{s.id}"
        ''',
    )
    for s in DOWNLOAD_SPECS
]
