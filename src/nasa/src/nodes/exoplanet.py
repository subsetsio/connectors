"""NASA Exoplanet Archive TAP (ADQL).

One Delta table per entity, streamed as `select * from <table>` CSV -> gzipped
csv raw. Streamed because some tables are wide/large (up to ~40k rows x 700
cols). Stateless full re-pull every run.
"""

from __future__ import annotations

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, get_client, raw_writer
from utils import retry

EXOPLANET_TABLES = [
    "ps", "pscomppars", "toi", "k2pandc", "ml", "stellarhosts", "TD",
    "CUMULATIVE", "Q1_Q17_DR25_KOI", "Q1_Q17_DR25_SUP_KOI", "Q1_Q17_DR25_TCE",
]


# spec id -> exact TAP table name (spec ids are lower/dashed and lose case)
def _spec_id(entity: str) -> str:
    return "nasa-" + entity.lower().replace("_", "-")


_EXO_BY_SPEC = {_spec_id(t): t for t in EXOPLANET_TABLES}

TAP_SYNC = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"


@retry
def fetch_exoplanet(node_id: str) -> None:
    asset = node_id
    table = _EXO_BY_SPEC[node_id]
    params = {"query": f"select * from {table}", "format": "csv"}
    client = get_client()
    # Stream straight to disk: tables range up to ~40k rows x 700 cols, too big
    # to hold the whole CSV in memory comfortably. Retry re-opens (overwrites).
    with raw_writer(asset, "csv.gz", mode="wt", compression="gzip") as out:
        with client.stream(
            "GET", TAP_SYNC, params=params,
            timeout=httpx.Timeout(600.0, connect=15.0),
        ) as resp:
            resp.raise_for_status()
            wrote_any = False
            for chunk in resp.iter_text():
                if chunk:
                    out.write(chunk)
                    wrote_any = True
    if not wrote_any:
        raise AssertionError(f"{asset}: TAP returned an empty body for {table}")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(t), fn=fetch_exoplanet, kind="download")
    for t in EXOPLANET_TABLES
]

# Exoplanet TAP tables: CSV is already richly typed by read_csv_auto; publish
# the table verbatim.
TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=f'SELECT * FROM "{s.id}"')
    for s in DOWNLOAD_SPECS
]
