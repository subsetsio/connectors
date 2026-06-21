"""Instituto Nacional de Estadísticas (Chile) — SDMX 2.1 connector.

Mechanism: dotStat SDMX 2.1 REST instance at https://sdmx.ine.gob.cl/rest,
single agency CL01. Each rank-accepted dataflow (DF_*) is pulled in full as
SDMX-CSV in one request and saved verbatim as a .csv raw asset. Columns vary
per dataflow (each has its own DSD: SEXO, EDAD, RAMA, CIUO88, UNIDAD, ...),
so the raw is stored as CSV and DuckDB auto-detects the schema per entity in
the transform.

Fetch shape: stateless full re-pull (shape 1). Each dataflow is tens of KB to
a few MB; the whole corpus is ~200 small requests, cheap to re-pull every run.
No incremental query, no state. Revisions are picked up for free.
"""

import pyarrow as pa  # noqa: F401  (kept for parity; not used directly here)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_file,
)
from constants import ENTITY_IDS

SLUG = "instituto-nacional-de-estad-sticas"
AGENCY = "CL01"
VERSION = "1.0"  # every CL01 dataflow is published at version 1.0 (verified)
BASE = "https://sdmx.ine.gob.cl/rest/data"

# Map each download node id back to its source dataflow id. Plain dict
# comprehension over an imported constant — no I/O, module-level is fine.
_NODE_TO_DF = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/transient network
def _fetch_csv(df_id: str) -> str:
    url = f"{BASE}/{AGENCY},{df_id},{VERSION}?format=csv"
    resp = get(
        url,
        headers={"Accept": "application/vnd.sdmx.data+csv"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()  # inside the retry; non-transient 4xx reraises
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    df_id = _NODE_TO_DF[node_id]
    csv_text = _fetch_csv(df_id)
    save_raw_file(csv_text, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataflow. DuckDB auto-detects the per-entity
# SDMX-CSV schema (OBS_VALUE -> DOUBLE, dimension codes -> VARCHAR/INTEGER,
# TIME_PERIOD kept as-is). All observation rows are kept — including blank
# OBS_VALUE cells (OBS_STATUS carries the reason), so a sparse series still
# publishes its full time grid rather than collapsing to zero rows.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
