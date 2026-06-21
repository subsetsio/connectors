"""National Records of Scotland — statistics.gov.scot (PublishMyData / SPARQL).

Catalog connector. Each rank-accepted entity is one RDF Data Cube
(qb:DataSet) published by NRS on statistics.gov.scot. Every observation
carries the standard dimensions refArea / refPeriod plus cube-specific
dimensions (gender, age, sex, council-tax-band, …) and a measure value
selected via qb:measureType.

Extraction is a stateless full re-pull per dataset. The SPARQL endpoint is
deliberately constrained — it hard-caps a single result set below 100k rows,
kills any query running past ~30s (multi-way joins and `?s ?p ?o` scans over a
large cube time out to an empty 200 or a 400 "Response too large"), and rejects
ORDER BY over multi-million-row sets. The only primitive that stays reliably
cheap is a *selective, few-pattern* scan keyset-paged by observation. So we:

  1. discover the cube's dimensions (its DataStructureDefinition) and the
     distinct refPeriod values,
  2. for each period, fetch the measure value and EACH dimension as its OWN
     keyset-paged 2-3 pattern query (<=50k rows/page, ORDER BY ?obs), and
  3. assemble the wide rows in Python by observation URI.

The period partition keeps every keyset scan small enough to sort, and the
per-column queries stay well under the server time limit. A per-period
COUNT(*) is verified against the rows assembled; a mismatch raises so a silent
truncation fails the node loudly instead of publishing a partial table.

No incremental query is supported (no since/modifiedAfter), so the full corpus
is re-pulled each refresh; the maintain step gates cadence.
"""
import csv
import io
import re
import time

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    post,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "national-records-of-scotland"
ENDPOINT = "https://statistics.gov.scot/sparql"
QB = "http://purl.org/linked-data/cube#"
MEASURE_TYPE = "http://purl.org/linked-data/cube#measureType"
REF_PERIOD = "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod"
# RDF resource identifier prefix — the http-scheme IRI the triplestore uses to
# identify each qb:DataSet (an opaque identifier, NOT a network URL; https would
# not match). All actual HTTP traffic goes to the https ENDPOINT above.
DATA_BASE = "http://statistics.gov.scot/data/"
PAGE = 50000  # endpoint caps a single result set below 100k rows

# Over a long run the shared httpx client pools one keep-alive connection across
# thousands of requests; nginx eventually closes it and the next reuse raises
# "Server disconnected without sending a response" (seen on cloud runs, never in
# short local runs). `Connection: close` forces a fresh connection per request,
# and a browser-style User-Agent avoids any UA filtering. Set once per process.
_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "close",
}
_http_configured = False

# Map each spec id back to its original-case dataset slug so the fetch fn can
# rebuild the qb:DataSet URI. Pure computation — no I/O at import.
ID_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


def _ensure_http():
    global _http_configured
    if not _http_configured:
        configure_http(headers=_HTTP_HEADERS)
        _http_configured = True


@transient_retry(attempts=8, max_wait=120)
def _sparql(query: str) -> list[dict]:
    """Run a SPARQL query via POST (avoids URL-length limits), CSV -> dicts.

    Retries transient network errors / 429 / 5xx with backoff.
    """
    _ensure_http()
    resp = post(
        ENDPOINT,
        data={"query": query},
        headers={"Accept": "text/csv"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return list(csv.DictReader(io.StringIO(resp.text)))


def _seg(uri):
    """Last path/fragment segment of a URI ('.../gender/all' -> 'all')."""
    if not uri:
        return uri
    return re.split(r"[/#]", uri.rstrip("/"))[-1]


def _col(uri: str) -> str:
    """Dimension URI -> snake_case column name (refArea -> ref_area)."""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", _seg(uri))
    return name.replace("-", "_").lower()


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _retry_nonempty(fn, what: str, ds_uri: str):
    """Discovery/count queries return empty under throttling; retry a few times
    before trusting an empty result."""
    for attempt in range(5):
        rows = fn()
        if rows:
            return rows
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"{ds_uri}: {what} returned empty after retries")


def _discover_dimensions(ds_uri: str) -> list[str]:
    rows = _retry_nonempty(
        lambda: _sparql(
            f"PREFIX qb: <{QB}> SELECT DISTINCT ?dim WHERE {{ "
            f"<{ds_uri}> qb:structure ?dsd . ?dsd qb:component ?c . "
            f"?c qb:dimension ?dim }}"
        ),
        "dimension discovery",
        ds_uri,
    )
    return [r["dim"] for r in rows if r["dim"] and r["dim"] != MEASURE_TYPE]


def _discover_periods(ds_uri: str) -> list[str]:
    rows = _retry_nonempty(
        lambda: _sparql(
            f"PREFIX qb: <{QB}> SELECT DISTINCT ?p WHERE {{ ?o qb:dataSet "
            f"<{ds_uri}> ; <{REF_PERIOD}> ?p }} ORDER BY ?p"
        ),
        "period discovery",
        ds_uri,
    )
    return [r["p"] for r in rows if r["p"]]


def _count(ds_uri: str, period_uri) -> int:
    where = f"?o qb:dataSet <{ds_uri}>"
    if period_uri:
        where += f" ; <{REF_PERIOD}> <{period_uri}>"
    rows = _retry_nonempty(
        lambda: _sparql(
            f"PREFIX qb: <{QB}> SELECT (COUNT(*) AS ?n) WHERE {{ {where} }}"
        ),
        "count",
        ds_uri,
    )
    return int(rows[0]["n"])


def _paged(select_vars: str, where_body: str) -> list[dict]:
    """Keyset-page a query whose first projected var is ?obs."""
    out = []
    last = None
    while True:
        flt = f'FILTER(STR(?obs) > "{_esc(last)}")' if last else ""
        rows = _sparql(
            f"PREFIX qb: <{QB}> SELECT {select_vars} WHERE {{ "
            f"{where_body} {flt} }} ORDER BY ?obs LIMIT {PAGE}"
        )
        if not rows:
            break
        out.extend(rows)
        last = rows[-1]["obs"]
        if len(rows) < PAGE:
            break
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    ds_uri = DATA_BASE + ID_TO_ENTITY[node_id]

    dims = _discover_dimensions(ds_uri)
    period_uri = REF_PERIOD if REF_PERIOD in dims else None
    other = [(d, _col(d)) for d in dims if d != period_uri]

    columns = (["ref_period"] if period_uri else []) + \
        [col for _uri, col in other] + ["measure_type", "value"]
    schema = pa.schema([(c, pa.string()) for c in columns])

    periods = _discover_periods(ds_uri) if period_uri else [None]

    with raw_parquet_writer(asset, schema) as writer:
        for pv in periods:
            expected = _count(ds_uri, pv)
            base = f"?obs qb:dataSet <{ds_uri}>"
            if pv:
                base += f" ; <{period_uri}> <{pv}>"

            # The measure value defines exactly one row per observation.
            value_rows = _paged(
                "?obs ?mt ?value",
                base + f" ; <{MEASURE_TYPE}> ?mt ; ?mt ?value .",
            )
            rowmap = {
                r["obs"]: {"measure_type": _seg(r["mt"]), "value": r["value"]}
                for r in value_rows
            }
            del value_rows

            # Each dimension joined in as its own cheap selective scan.
            for uri, col in other:
                for r in _paged("?obs ?v", base + f" ; <{uri}> ?v ."):
                    rec = rowmap.get(r["obs"])
                    if rec is not None:
                        rec[col] = _seg(r["v"])

            if len(rowmap) != expected:
                raise RuntimeError(
                    f"{asset}: period {pv} assembled {len(rowmap)} rows, "
                    f"expected {expected} — likely a truncated/timed-out page; "
                    f"failing to avoid silent truncation"
                )
            if not rowmap:
                continue

            batch = []
            period_seg = _seg(pv) if pv else None
            for rec in rowmap.values():
                row = {}
                if period_uri:
                    row["ref_period"] = period_seg
                for _uri, col in other:
                    row[col] = rec.get(col)
                row["measure_type"] = rec["measure_type"]
                row["value"] = rec["value"]
                batch.append(row)
            writer.write_table(pa.Table.from_pylist(batch, schema=schema))
            del rowmap, batch


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
