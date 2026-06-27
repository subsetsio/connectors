"""Open Power System Data (OPSD) connector — node module.

OPSD publishes Frictionless tabular-data-packages on its data platform. Each
collect entity is one CSV resource, identified as `<package>__<resource_stem>`,
served at:

    https://data.open-power-system-data.org/<package>/latest/<resource_stem>.csv

Fetch shape: **stateless full re-pull** (shape 1). Every CSV is a complete
snapshot of its table; OPSD releases new versions infrequently (roughly annual)
under the moving `latest/` alias, so each run re-downloads the current snapshot
in full and overwrites — no watermark, no incremental filter (the source exposes
none). The biggest table (hourly time_series, ~50k rows × 300 cols) is ~123MB in
memory, comfortably in RAM.

Raw format: the CSVs are clean, comma-delimited, single-header tabular files, but
schemas vary widely (13 to 656 columns) and many columns are sparse. We let
DuckDB infer types over the *whole* file (`sample_size=-1`, which falls back to
VARCHAR on genuinely mixed columns rather than erroring) and write the result as
parquet. The SQL transform is then a thin pass-through that publishes the typed
table verbatim.
"""

import os
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "open-power-system-data"
BASE = "https://data.open-power-system-data.org"


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# spec id -> original-cased collect entity id (the lower/replace mapping is lossy,
# so we keep the reverse map explicitly). Plain dict comprehension, no I/O.
ENTITY_BY_SPEC = {_spec_id(eid): eid for eid in ENTITY_IDS}


@transient_retry()
def _download_csv(url: str) -> bytes:
    # read timeout generous: the largest CSV (time_series_60min) is ~130MB.
    resp = get(url, timeout=(15.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = ENTITY_BY_SPEC[node_id]
    package, stem = entity_id.split("__", 1)
    url = f"{BASE}/{package}/latest/{stem}.csv"

    content = _download_csv(url)

    # Write to a scratch temp file so DuckDB can do full-file type inference,
    # then convert to an Arrow table (the Arrow path avoids the timezone->python
    # datetime materialization that needs pytz). This is scratch I/O, not raw
    # persistence — the raw asset is written via save_raw_parquet below.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        safe_path = tmp_path.replace("'", "''")
        con = duckdb.connect()
        try:
            table = con.execute(
                f"SELECT * FROM read_csv_auto('{safe_path}', sample_size=-1)"
            ).fetch_arrow_table()
        finally:
            con.close()
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per subset: a thin pass-through of the typed parquet.
# (Schemas are already clean from DuckDB inference; renaming/casting 13-to-656
# heterogeneous columns per table would be noise, not correctness.)
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
