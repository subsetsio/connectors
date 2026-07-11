"""MTA Open Data connector.

Source: MTA datasets published on New York State's Socrata portal (data.ny.gov),
grouped by attribution="Metropolitan Transportation Authority". Each accepted
rank entity is one Socrata dataset identified by a persistent 4x4 id (e.g.
``wujg-7c2s``).

Fetch shape: stateless full re-pull. Socrata's per-resource CSV export
(``/resource/<id>.csv?$limit=<all>``) streams the entire table in a single
request, so each refresh streams the whole dataset straight to a gzip'd raw CSV
(in cloud mode raw_writer streams directly to R2 via multipart — no large local
files). There is no portal-wide incremental cursor and column names differ per
dataset, so a uniform delta filter is not available; full snapshots pick up
revisions for free. A few datasets are large (the hourly-ridership and
origin-destination tables run to ~120M rows) — the single streamed export is the
efficient bulk path for those (no deep-offset pagination), and transient_retry
restarts a dropped stream.

Transform: one thin SqlNodeSpec per dataset — ``SELECT * FROM "<download>"`` over
the CSV view (DuckDB ``read_csv_auto``), published 1:1 as a Delta table.
"""

import os

from subsets_utils import NodeSpec, get_client, raw_writer, transient_retry

from constants import ENTITY_IDS

PREFIX = "mta-open-data-"
RESOURCE_BASE = "https://data.ny.gov/resource"
# $limit larger than any MTA table — Socrata streams the full CSV export in one
# response when the limit covers every row (no server-side pagination).
EXPORT_LIMIT = 1_000_000_000
CHUNK = 1 << 20  # 1 MiB


def _resource_id(node_id: str) -> str:
    """Recover the Socrata 4x4 id from a download node id."""
    return node_id[len(PREFIX):]


@transient_retry()
def _stream_export(resource_id: str, asset: str) -> None:
    """Stream the full CSV export for one dataset to a gzip'd raw asset.

    Opens the writer fresh on each attempt so a retry overwrites a partial file
    rather than appending to it.
    """
    url = f"{RESOURCE_BASE}/{resource_id}.csv"
    params = {"$limit": EXPORT_LIMIT}
    headers = {}
    token = os.environ.get("SOCRATA_APP_TOKEN")
    if token:
        headers["X-App-Token"] = token  # optional; avoids throttling on big pulls

    client = get_client()
    with raw_writer(asset, extension="csv.gz", mode="wb", compression="gzip") as out:
        with client.stream(
            "GET", url, params=params, headers=headers, timeout=(10.0, 300.0)
        ) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_bytes(chunk_size=CHUNK):
                out.write(chunk)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _stream_export(_resource_id(node_id), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"mta-open-data-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
