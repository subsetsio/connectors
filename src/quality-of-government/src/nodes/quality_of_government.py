"""Quality of Government Institute (QoG), University of Gothenburg.

Bulk-CSV source. Each subset is one whole-table CSV served at
https://www.qogdata.pol.gu.se/data/ as ``qog_<dataset>_<dim>_<release>.csv``.
There is no queryable API and no incremental filter, and each file is wholly
delivered in a single GET (a few hundred KB to ~90MB), so every node does a
**stateless full re-pull**: fetch the CSV, parse it, overwrite the raw parquet.
The source refreshes roughly annually; a refresh re-fetches the whole file.

URL stability: the ``<release>`` tag is baked into each filename (jan26 / nov20 /
sept21 / 24) and there is no redirecting "latest" alias, so the current filename
per entity is pinned in ``ENTITY_FILES`` below. When QoG ships a new release,
bump the relevant filename(s) here.

Raw format: the tables are wide (ID columns like ccode/cname plus up to ~2100
governance variables), so an explicit pa.schema is impractical to hand-declare.
Each asset is a single one-shot write of a fully-materialised file, so we let
``pyarrow.csv`` infer one type per column over the whole file (it reads the file
end-to-end before finalising types — no chunked misinference) and write the
result straight to parquet. The SQL transform is then a thin ``SELECT *`` pass
that republishes the typed table as a Delta table (and fails loudly on an empty
payload). pyarrow (not pandas) keeps the node off numpy, which the spec-dump
introspection context can't import cleanly.
"""
import io

import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "quality-of-government"
BASE = "https://www.qogdata.pol.gu.se/data/"

# entity_id -> current release filename (verified 200 text/csv during research).
# Bump these when QoG publishes a new release (the release tag is in the name).
ENTITY_FILES = {
    "qog_std_ts": "qog_std_ts_jan26.csv",
    "qog_std_cs": "qog_std_cs_jan26.csv",
    "qog_bas_ts": "qog_bas_ts_jan26.csv",
    "qog_bas_cs": "qog_bas_cs_jan26.csv",
    "qog_oecd_ts": "qog_oecd_ts_jan26.csv",
    "qog_oecd_cs": "qog_oecd_cs_jan26.csv",
    "qog_ei_ts": "qog_ei_ts_sept21.csv",
    "qog_eureg_long": "qog_eureg_long_nov20.csv",
    "qog_eureg_wide1": "qog_eureg_wide1_nov20.csv",
    "qog_eureg_wide2": "qog_eureg_wide2_nov20.csv",
    "qog_eqi_long": "qog_eqi_long_24.csv",
    "qog_eqi_ind": "qog_eqi_ind_24.csv",
    "qog_eqicati_long": "qog_eqicati_long_24.csv",
}


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _entity_id_from_node(node_id: str) -> str:
    # quality-of-government-qog-std-ts -> qog_std_ts
    return node_id[len(SLUG) + 1:].replace("-", "_")


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = _entity_id_from_node(node_id)
    filename = ENTITY_FILES[entity_id]  # KeyError = bug; surface it
    content = _fetch_bytes(BASE + filename)

    # pyarrow infers one type per column over the whole file; no schema to
    # hand-declare for a ~2100-column table, and no chunked misinference.
    table = pacsv.read_csv(io.BytesIO(content))
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_FILES
]

# Thin parse-and-publish: republish each fetched table verbatim as a Delta
# table. The runtime overwrites the table named <id minus -transform>; a 0-row
# result fails the node, so this also guards against a truncated download.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
