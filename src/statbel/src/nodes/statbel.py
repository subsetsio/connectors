"""Statbel (Statistics Belgium) — open-data corpus.

One published Delta table per Statbel DCAT dataset node. Each download node
resolves its dataset's current download URL from a fresh read of the DCAT-BE
catalogue, fetches the delimited-text distribution (.zip of pipe-delimited
TXT, .csv, .csv.zip or .gz), and parses it to NDJSON rows of strings. The
per-dataset schemas are heterogeneous, so the transform is a thin passthrough
that publishes the table as-is.

Fetch shape: stateless full re-pull. Files are modest (~0.5-3MB each) and
Statbel exposes no incremental download filter, so every run re-reads the
catalogue and re-fetches each dataset in full and overwrites.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from constants import ENTITY_IDS
from utils import fetch_rows


def _spec_id(entity_id: str) -> str:
    return f"statbel-{entity_id.lower().replace('_', '-')}"


# Map the lowercased spec id back to the source's original node identifier
# (the catalogue is keyed by the mixed-case "NodeID####").
_ID_BY_SPEC = {_spec_id(e): e for e in ENTITY_IDS}


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = _ID_BY_SPEC[node_id]
    rows = fetch_rows(entity_id)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
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
