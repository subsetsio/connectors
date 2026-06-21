"""Scottish Government Statistics (statistics.gov.scot) — RDF Data Cube connector.

statistics.gov.scot is a PublishMyData (Swirrl) linked-data platform. The
statistical content lives in 276 W3C RDF Data Cubes (qb:DataSet); the rank step
accepted 181 of them (the file-dataset blobs were demoted). Every cube uses the
SDMX measure-dimension pattern, so a single generic extractor works for all of
them:

  * discover the cube's dimensions from its DSD (qb:structure/qb:component),
  * project one row per observation — each dimension value, the measure name
    (qb:measureType), the measure value, and the unitMeasure attribute,
  * paginate with LIMIT/OFFSET.

Pagination notes (verified against the live endpoint):
  * The endpoint enforces a ~30s server timeout. ORDER BY over a multi-million
    -row cube blows that budget, so we paginate WITHOUT ORDER BY. The store's
    scan order is deterministic (an identical query returns byte-identical rows),
    so OFFSET paging is stable; the only artdefact is the occasional boundary
    observation that carries two measure rows straddling a page edge, which the
    transform removes with SELECT DISTINCT.
  * A projected (joined) row hits the result-size cap around 25k rows, so we use
    a 20000-row page.

Fetch shape: stateless full re-pull. Each cube is re-extracted in full every run
and overwritten downstream — revisions are picked up for free. There is no
incremental delta filter on the data (only dct:modified per dataset, used for
change detection elsewhere), so full corpus per refresh is the only option.
Large cubes (up to ~8M observations) are streamed to gzip'd NDJSON so memory
stays bounded.
"""

import csv
import io
import json
import re

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer, transient_retry
from constants import CUBE_IDS

SPARQL = "https://statistics.gov.scot/sparql"
PAGE = 20000
MAX_PAGES = 2000  # safety backstop: 40M rows. Raises if exceeded.

QB = "http://purl.org/linked-data/cube#"
SDMX_DIM = "http://purl.org/linked-data/sdmx/2009/dimension#"
SDMX_ATTR = "http://purl.org/linked-data/sdmx/2009/attribute#"

# download id -> original-case dataset slug (statistics.gov.scot URIs are
# case-sensitive, and the spec id lowercases the slug).
SLUG_BY_ID = {
    f"scottish-government-statistics-{eid.lower().replace('_', '-')}": eid
    for eid in CUBE_IDS
}


def _local(uri: str) -> str:
    """Last path/fragment segment of a URI (the human-readable code/name)."""
    return re.sub(r"^.*[/#]", "", uri)


@transient_retry()
def _sparql_csv(query: str) -> str:
    resp = get(
        SPARQL,
        params={"query": query},
        headers={"Accept": "text/csv"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.text


def _rows(query: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(_sparql_csv(query))))


def _discover_dimensions(ds_uri: str) -> list[str]:
    """Dimension property URIs for a cube, excluding qb:measureType."""
    q = (
        f"PREFIX qb: <{QB}>\n"
        "SELECT DISTINCT ?dim WHERE { <%s> qb:structure/qb:component/qb:dimension ?dim\n"
        "  FILTER(?dim != qb:measureType) }" % ds_uri
    )
    return [r["dim"] for r in _rows(q)]


def _column_names(dim_uris: list[str]) -> list[str]:
    """Local-name per dimension, de-duplicated against collisions and reserved
    output columns (measure/value/unit)."""
    reserved = {"measure", "value", "unit"}
    names, seen = [], set(reserved)
    for uri in dim_uris:
        base = _local(uri)
        name = base
        i = 1
        while name in seen:
            i += 1
            name = f"{base}_{i}"
        seen.add(name)
        names.append(name)
    return names


def _page_query(ds_uri: str, dim_uris: list[str], cols: list[str], offset: int) -> str:
    select = ["?measure", "?value", "?unit"] + [f"?{c}" for c in cols]
    where = [
        f"?o qb:dataSet <{ds_uri}> ; qb:measureType ?mU ; ?mU ?value .",
        f"OPTIONAL {{ ?o <{SDMX_ATTR}unitMeasure> ?unitU }}",
    ]
    binds = [
        'BIND(REPLACE(STR(?mU),"^.*[/#]","") AS ?measure)',
        'BIND(REPLACE(STR(?unitU),"^.*[/#]","") AS ?unit)',
    ]
    for col, uri in zip(cols, dim_uris):
        where.append(f"?o <{uri}> ?{col}U .")
        binds.append(f'BIND(REPLACE(STR(?{col}U),"^.*[/#]","") AS ?{col})')
    return (
        f"PREFIX qb: <{QB}>\n"
        f"SELECT {' '.join(select)} WHERE {{\n"
        + "\n".join(where)
        + "\n"
        + "\n".join(binds)
        + f"\n}} LIMIT {PAGE} OFFSET {offset}"
    )


def _coerce_value(raw: str):
    """Measure values are numeric; keep them as floats so the published column is
    typed. Anything non-numeric falls through as the original string."""
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return raw


def fetch_cube(node_id: str) -> None:
    eid = SLUG_BY_ID[node_id]
    ds_uri = f"http://statistics.gov.scot/data/{eid}"
    dim_uris = _discover_dimensions(ds_uri)
    cols = _column_names(dim_uris)

    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for page in range(MAX_PAGES):
            rows = _rows(_page_query(ds_uri, dim_uris, cols, page * PAGE))
            if not rows:
                break
            for r in rows:
                out = {
                    "measure": r.get("measure") or None,
                    "value": _coerce_value(r.get("value")),
                    "unit": r.get("unit") or None,
                }
                for c in cols:
                    out[c] = r.get(c) or None
                f.write(json.dumps(out, separators=(",", ":")) + "\n")
            written += len(rows)
            if len(rows) < PAGE:
                break
        else:
            raise RuntimeError(
                f"{node_id}: hit MAX_PAGES={MAX_PAGES} ({written} rows) — cube larger "
                "than expected; raise the cap or chunk by refPeriod."
            )
    print(f"  {node_id}: {written:,} observations across {len(cols)} dimensions")


DOWNLOAD_SPECS = [
    NodeSpec(id=node_id, fn=fetch_cube, kind="download")
    for node_id in SLUG_BY_ID
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT DISTINCT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
