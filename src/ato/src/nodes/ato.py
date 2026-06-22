"""ATO connector — data.gov.au CKAN catalog.

Each entity is a recurring ATO statistical table, collapsed across its
per-income-year editions (one CKAN resource per year). We pull every year's
flat table from the CKAN **datastore** (`datastore_search`, which returns the
resource as typed-as-text rows), tag each row with its `income_year`, and write
the union as one NDJSON raw asset. NDJSON (not parquet) because column sets
drift across years for the same table — datastore field lists are not stable
edition-to-edition, so a fixed schema would be wrong.

Fetch shape: **stateless full re-pull** (decision shape 1). The whole corpus is
small (datastore tables are tens of thousands of rows at most) and the source
exposes no useful per-record delta filter, so every refresh re-pulls in full and
overwrites — late ATO revisions are picked up for free.

The transform is a thin pass-through: datastore values are all text and the
209 tables are mutually heterogeneous, so generic per-column typing isn't
possible here; the SQL publishes the unioned rows as-is (light reshape only).
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from constants import ENTITY_IDS
from utils import build_groups, datastore_rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("ato-"):]

    groups = build_groups()
    resources = groups.get(entity_id)
    if not resources:
        # coverage is validated up front, so a miss here means the catalog
        # grouping drifted from collect — a bug, not a transient condition.
        raise RuntimeError(f"{node_id}: entity {entity_id!r} not found in live catalog")

    def _rows():
        for res in resources:
            if not res["datastore_active"]:
                continue  # only datastore-backed editions are flat-readable
            yield from datastore_rows(res["resource_id"], res["income_year"])

    save_raw_ndjson(_rows(), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ato-{eid.lower().replace('_', '-')}",
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
