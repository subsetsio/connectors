"""National Records of Scotland — statistics.gov.scot (PublishMyData / SPARQL).

Catalog connector. Each rank-accepted entity is one RDF Data Cube
(qb:DataSet) published by NRS on statistics.gov.scot. Every observation
carries the standard dimensions refArea / refPeriod plus cube-specific
dimensions (gender, age, sex, council-tax-band, …) and one or more
measures selected via qb:measureType.

Extraction is a generic, fully stateless full re-pull per dataset:
  1. discover the cube's dimensions from its DataStructureDefinition,
  2. discover the distinct refPeriod values (years),
  3. for each period, keyset-page the observations (ORDER BY ?obs,
     FILTER ?obs > last) in <=50k-row pages — the SPARQL endpoint hard-caps
     a single result set below 100k rows, and an unpartitioned ORDER BY over
     a multi-million-row cube silently times out to an empty 200, so the
     period partition keeps every ordered subset small enough to sort.

A per-period COUNT(*) is verified against the rows actually pulled; a
mismatch raises so a silent truncation fails the node loudly instead of
publishing a partial table.

No incremental query is supported by the endpoint (no since/modifiedAfter),
so the full corpus is re-pulled each refresh; the maintain step gates cadence.
"""
import csv
import io
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "national-records-of-scotland"
SPARQL = "https://statistics.gov.scot/sparql.csv"
QB = "http://purl.org/linked-data/cube#"
MEASURE_TYPE = "http://purl.org/linked-data/cube#measureType"
REF_PERIOD = "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod"
# RDF resource identifier prefix. This is the http-scheme IRI the triplestore
# uses to identify each qb:DataSet (an opaque identifier, NOT a network URL) —
# https would not match. All actual HTTP traffic goes to the https SPARQL
# endpoint above.
DATA_BASE = "http://statistics.gov.scot/data/"
PAGE = 50000  # endpoint caps a single result set below 100k rows

# Map each spec id (lower-cased) back to its original-case dataset slug so the
# fetch fn can rebuild the qb:DataSet URI. Pure computation — no I/O at import.
ID_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()
def _sparql(query: str) -> list[dict]:
    """Run a SPARQL query, returning CSV rows as dicts. Retries transient errors."""
    resp = get(
        SPARQL,
        params={"query": query},
        headers={"Accept": "text/csv"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return list(csv.DictReader(io.StringIO(resp.text)))


def _seg(uri: str) -> str:
    """Last path/fragment segment of a URI ('.../gender/all' -> 'all')."""
    if uri is None:
        return None
    return re.split(r"[/#]", uri.rstrip("/"))[-1] if uri else uri


def _snake(name: str) -> str:
    """camelCase / kebab-case URI segment -> snake_case column name."""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.replace("-", "_").lower()


def _discover_dimensions(ds_uri: str) -> list[str]:
    """Dimension property URIs of the cube (excludes qb:measureType)."""
    rows = _sparql(
        f"PREFIX qb: <{QB}> "
        f"SELECT DISTINCT ?dim WHERE {{ <{ds_uri}> qb:structure ?dsd . "
        f"?dsd qb:component ?c . ?c qb:dimension ?dim }}"
    )
    return [r["dim"] for r in rows if r["dim"] and r["dim"] != MEASURE_TYPE]


def _discover_periods(ds_uri: str) -> list[str]:
    """Distinct refPeriod value URIs for the cube, ascending."""
    rows = _sparql(
        f"PREFIX qb: <{QB}> "
        f"SELECT DISTINCT ?p WHERE {{ ?o qb:dataSet <{ds_uri}> ; "
        f"<{REF_PERIOD}> ?p }} ORDER BY ?p"
    )
    return [r["p"] for r in rows if r["p"]]


def _count(ds_uri: str, period_uri: str | None) -> int:
    where = f"?o qb:dataSet <{ds_uri}>"
    if period_uri:
        where += f" ; <{REF_PERIOD}> <{period_uri}>"
    rows = _sparql(
        f"PREFIX qb: <{QB}> SELECT (COUNT(*) AS ?n) WHERE {{ {where} }}"
    )
    return int(rows[0]["n"])


def _page_query(ds_uri, period_uri, period_val, other_dims, last_obs):
    """One keyset page of observations for a (dataset, period) partition."""
    lines = [f"?obs qb:dataSet <{ds_uri}> ;"]
    if period_uri and period_val:
        lines.append(f"  <{period_uri}> <{period_val}> ;")
    lines.append("  qb:measureType ?mt ; ?mt ?value .")
    sel = ["?obs", "?value", "?mt"]
    for i, (uri, _col) in enumerate(other_dims):
        var = f"?d{i}"
        lines.append(f"OPTIONAL {{ ?obs <{uri}> {var} }}")
        sel.append(var)
    if last_obs:
        # last_obs comes from server-returned IRIs; quote-escape defensively.
        safe = last_obs.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'FILTER(STR(?obs) > "{safe}")')
    return (
        f"PREFIX qb: <{QB}>\n"
        f"SELECT {' '.join(sel)} WHERE {{\n" + "\n".join(lines) + "\n}\n"
        f"ORDER BY ?obs LIMIT {PAGE}"
    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = ID_TO_ENTITY[node_id]
    ds_uri = DATA_BASE + entity

    dims = _discover_dimensions(ds_uri)
    period_uri = next((d for d in dims if d == REF_PERIOD), None)
    other_dims = [(d, _snake(_seg(d))) for d in dims if d != period_uri]

    columns = (["ref_period"] if period_uri else []) + \
        [col for _uri, col in other_dims] + ["measure_type", "value"]
    schema = pa.schema([(c, pa.string()) for c in columns])

    periods = _discover_periods(ds_uri) if period_uri else [None]
    if not periods:
        raise RuntimeError(f"{asset}: cube has refPeriod but no period values")

    with raw_parquet_writer(asset, schema) as writer:
        for period_val in periods:
            expected = _count(ds_uri, period_val)
            got = 0
            last_obs = None
            while True:
                rows = _sparql(
                    _page_query(ds_uri, period_uri, period_val, other_dims, last_obs)
                )
                if not rows:
                    break
                batch = []
                for r in rows:
                    rec = {}
                    if period_uri:
                        rec["ref_period"] = _seg(period_val)
                    for i, (_uri, col) in enumerate(other_dims):
                        rec[col] = _seg(r.get(f"d{i}"))
                    rec["measure_type"] = _seg(r.get("mt"))
                    rec["value"] = r.get("value")
                    batch.append(rec)
                writer.write_table(pa.Table.from_pylist(batch, schema=schema))
                got += len(rows)
                last_obs = rows[-1]["obs"]
                if len(rows) < PAGE:
                    break
            if got != expected:
                raise RuntimeError(
                    f"{asset}: period {period_val} pulled {got} rows, "
                    f"expected {expected} (likely a server-side ORDER BY timeout "
                    f"returning an empty page) — failing to avoid silent truncation"
                )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Uniform thin transform: cast the measure value to DOUBLE (keeping every
# cube-specific dimension column via SELECT * REPLACE) and drop non-numeric /
# missing values. One published Delta table per cube.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=(
            f'SELECT * REPLACE (TRY_CAST(value AS DOUBLE) AS value) '
            f'FROM "{s.id}" WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL'
        ),
    )
    for s in DOWNLOAD_SPECS
]
