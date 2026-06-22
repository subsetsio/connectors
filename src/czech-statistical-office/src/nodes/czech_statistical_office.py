"""Czech Statistical Office (ČSÚ / CZSO) open-data connector.

Catalog connector over CZSO's CKAN-style open-data API. Each rank-accepted
dataset is a single full CSV published at csu.gov.cz, discovered via the CKAN
`package_show` resource list on vdb.czso.cz. The CSVs are long-format
observation tables (one row per coded observation) with per-dataset column
sets; encoding is UTF-8, comma-delimited, double-quoted, header present
(verified across diverse datasets while probing).

Fetch shape: **stateless full re-pull** (decision shape 1). Each dataset is a
single CSV of at most a few tens of MB and there is no incremental query
filter on the CKAN API, so every run re-fetches the whole CSV and overwrites.
Freshness gating is the maintain step's job.

Raw format: the CSV is saved verbatim as an opaque file (`save_raw_file`,
extension "csv"). Column sets differ per dataset, so the transform is a generic
passthrough that lets DuckDB infer types from each dataset's own CSV — a thin
parse/type pass, which is the only scalable shape across 233 heterogeneous
tables.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_file,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "czech-statistical-office"
CKAN_BASE = "https://vdb.czso.cz/pll/eweb"

# spec id (lossy: lower + '_'->'-') back to the source's original dataset id.
_SPEC_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _package_show(entity_id: str) -> dict:
    resp = get(
        f"{CKAN_BASE}/package_show",
        params={"id": entity_id},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()["result"]


@transient_retry()
def _download_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _pick_csv_resource(resources: list) -> dict:
    """Pick the dataset's CSV distribution. Every probed dataset exposes exactly
    one text/csv resource; prefer an explicit csv format, else the sole
    resource. Raise loudly if there's nothing CSV-shaped to fetch."""
    csv_res = [
        r for r in resources
        if "csv" in (r.get("format") or "").lower()
        or (r.get("url") or "").lower().split("?")[0].endswith(".csv")
    ]
    if csv_res:
        return csv_res[0]
    if len(resources) == 1:
        return resources[0]
    raise RuntimeError(
        f"no CSV resource among {len(resources)} resources: "
        f"{[r.get('format') for r in resources]}"
    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = _SPEC_TO_ENTITY[node_id]

    rec = _package_show(entity_id)
    resources = rec.get("resources") or []
    if not resources:
        raise RuntimeError(f"{entity_id}: package_show returned no resources")

    res = _pick_csv_resource(resources)
    content = _download_csv(res["url"])
    # CZSO serves UTF-8; normalize any stray BOM so DuckDB reads clean headers.
    if content[:3] == b"\xef\xbb\xbf":
        content = content[3:]
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. Column sets differ per dataset, so the
# transform is a generic passthrough: DuckDB reads each dataset's CSV view and
# infers types. A 0-row result fails the node, guarding against empty/truncated
# downloads.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
