"""ParlGov connector — Parliament and Government Database (parties, elections,
cabinets for all EU + most OECD democracies, 1945-present).

Mechanism: bulk_csv. One stable CSV per table at
https://parlgov.fly.dev/data-csv/<table>/ (trailing slash; the server 301s the
unslashed form). The whole corpus is a few MB, so the shape is a stateless full
re-pull every run — no incremental query exists on the CSV path and the source
publishes revisions in place. Each table's full CSV is fetched, parsed, and
written as NDJSON with raw string cell values (empty string -> null); the SQL
transforms own all typing via explicit casts, which keeps the raw layer
schema-stable and pushes the correctness gate into DuckDB.
"""

import csv
import io


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://parlgov.fly.dev/data-csv"

# Entity union — the rank-active ParlGov tables/views (see work/entity_union.json).
ENTITY_IDS = [
    "data_cabinet",
    "data_cabinet_party",
    "data_code",
    "data_country",
    "data_election",
    "data_election_result",
    "data_party",
    "data_party_change",
    "data_party_family",
    "data_party_name_change",
    "view_cabinet",
    "view_election",
    "view_party",
]


def _fetch_csv_text(table: str) -> str:
    resp = get(f"{BASE}/{table}/", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id  # runtime passes the spec id; it is also the asset name
    table = node_id[len("parlgov-"):].replace("-", "_")
    text = _fetch_csv_text(table)
    reader = csv.DictReader(io.StringIO(text))
    # Keep every cell as a raw string; collapse empty strings to null so the
    # transform's CAST sees real NULLs instead of failing on "".
    rows = [
        {k: (v if v not in ("", None) else None) for k, v in row.items()}
        for row in reader
    ]
    if not rows:
        raise AssertionError(f"{table}: CSV parsed to 0 rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"parlgov-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
