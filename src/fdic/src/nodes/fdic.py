"""FDIC BankFind Suite connector.

One download spec per FDIC API dataset endpoint (institutions, financials,
locations, history, failures, sod, summary, demographics). Each endpoint is a
distinct dataset with its own schema, so each publishes one Delta table.

Fetch shape: stateless full re-pull. Every endpoint is paged in full each run
(limit=10000 + incrementing offset until `meta.total` is reached) and written
as parquet with an explicit, curated, typed column projection. Projecting a
known column set up front (rather than dumping all 33-254 raw fields as
auto-inferred ndjson) keeps the published tables clean and removes any
type-inference ambiguity on the large financials endpoint (~1.68M rows), which
is streamed page-by-page to stay memory-bounded.

API: https://api.fdic.gov/banks  (no auth; offset pagination; max limit 10000).
Envelope: {"meta": {"total": N, ...}, "data": [{"data": {...}, "score": ...}]}.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://api.fdic.gov/banks"
PAGE_SIZE = 10000
MAX_PAGES = 1000  # safety ceiling per partition (1000 * 10000 = 10M rows)

# The API is Elasticsearch-backed with a hard result window of 2,000,000:
# any request whose offset+limit would exceed it returns HTTP 400. Endpoints
# larger than this must be paged in partitions each under the window. Only
# `sod` (~2.82M rows) currently exceeds it; it is partitioned by YEAR
# (~85k rows/year). financials (~1.68M) and demographics (~1.66M) are under
# the window and paged whole — the WINDOW guard below fails loudly (rather
# than truncating) if either ever grows past it.
RESULT_WINDOW = 2_000_000

# Endpoints paged in partitions, with the field whose distinct values define
# the partitions. Keyed by the bare endpoint name. Everything not listed is
# paged as a single partition.
PARTITION_FIELD = {"sod": "YEAR"}

# Per-endpoint curated column projection. Each value maps FDIC field name ->
# logical type: "s" = string (identifiers, codes, names, dates, geography),
# "f" = float64 (counts, money, ratios, coordinates). float64 is a safe
# superset for FDIC numeric fields, which mix integer and decimal values.
COLUMNS: dict[str, dict[str, str]] = {
    "institutions": {
        "CERT": "s", "NAME": "s", "CITY": "s", "STALP": "s", "STNAME": "s",
        "ZIP": "s", "COUNTY": "s", "ADDRESS": "s", "BKCLASS": "s",
        "CHARTER": "s", "CHRTAGNT": "s", "REGAGNT": "s", "FED_RSSD": "s",
        "UNINUM": "s", "ACTIVE": "f", "ESTYMD": "s", "ENDEFYMD": "s",
        "INSDATE": "s", "WEBADDR": "s", "MDI_STATUS_DESC": "s",
        "CBSA_METRO_NAME": "s", "CSA": "s", "RISDATE": "s",
        "LATITUDE": "f", "LONGITUDE": "f",
    },
    "financials": {
        "CERT": "s", "NAME": "s", "REPDTE": "s", "RISDATE": "s", "STALP": "s",
        "CITY": "s", "BKCLASS": "s", "ASSET": "f", "DEP": "f", "DEPDOM": "f",
        "DEPINS": "f", "DEPUNINS": "f", "LIAB": "f", "EQ": "f", "EQTOT": "f",
        "NETINC": "f", "ROA": "f", "ROE": "f", "NIM": "f", "NUMEMP": "f",
        "LNLSNET": "f", "INTINC": "f", "INTEXPY": "f",
    },
    "locations": {
        "CERT": "s", "NAME": "s", "UNINUM": "s", "OFFNAME": "s", "OFFNUM": "f",
        "MAINOFF": "f", "ADDRESS": "s", "CITY": "s", "STALP": "s",
        "STNAME": "s", "ZIP": "s", "COUNTY": "s", "SERVTYPE": "f",
        "SERVTYPE_DESC": "s", "ESTYMD": "s", "ACQDATE": "s",
        "CBSA_METRO_NAME": "s", "LATITUDE": "f", "LONGITUDE": "f",
    },
    "history": {
        "ID": "s", "CERT": "s", "INSTNAME": "s", "CHANGECODE": "s",
        "CHANGECODE_DESC": "s", "EFFDATE": "s", "EFFYEAR": "s",
        "PROCDATE": "s", "CLASS": "s", "CLASS_TYPE_DESC": "s", "PCITY": "s",
        "PSTALP": "s", "TRANSNUM": "s", "FDICREGION_DESC": "s", "ORGTYPE": "s",
    },
    "failures": {
        "ID": "s", "CERT": "s", "NAME": "s", "CITY": "s", "PSTALP": "s",
        "CITYST": "s", "FAILDATE": "s", "FAILYR": "s", "RESTYPE": "s",
        "RESTYPE1": "s", "QBFASSET": "f", "QBFDEP": "f", "COST": "f",
        "SAVR": "s", "CHCLASS1": "s", "BIDNAME": "s", "FUND": "s",
    },
    "sod": {
        "ID": "s", "CERT": "s", "NAMEFULL": "s", "NAMEBR": "s", "YEAR": "s",
        "STALPBR": "s", "CITYBR": "s", "CNTYNAMB": "s", "ZIPBR": "s",
        "DEPSUMBR": "f", "DEPSUM": "f", "DEPDOM": "f", "ASSET": "f",
        "BKCLASS": "s", "BRSERTYP": "f", "BRNUM": "f", "ADDRESBR": "s",
        "SIMS_LATITUDE": "f", "SIMS_LONGITUDE": "f",
    },
    "summary": {
        "YEAR": "s", "STALP": "s", "STNAME": "s", "BANKS": "f", "OFFICES": "f",
        "BRANCHES": "f", "ASSET": "f", "DEP": "f", "DEPDOM": "f", "LIAB": "f",
        "EQ": "f", "NETINC": "f", "LNLS": "f", "LNLSNET": "f", "NUMEMP": "f",
        "TOTAL": "f",
    },
    "demographics": {
        "ID": "s", "CERT": "s", "REPDTE": "s", "CALLYM": "s", "QTRNO": "f",
        "CBSANAME": "s", "CNTRYALP": "s", "CNTYNUM": "s", "MNRTYCDE": "s",
        "MNRTYDTE": "s", "BRANCH": "f", "OFFTOT": "f", "OFFNDOM": "f",
        "OFFOTH": "f", "OFFSTATE": "f", "METRO": "f", "MICRO": "f",
        "DIVISION": "f", "FDICTERR": "s", "FDICAREA": "f",
        "SIMS_LAT": "f", "SIMS_LONG": "f",
    },
}

_PA_TYPE = {"s": pa.string(), "f": pa.float64()}


# ---- transport ---------------------------------------------------------


@transient_retry()
def _api(endpoint: str, **params) -> dict:
    params.setdefault("format", "json")
    resp = get(f"{BASE}/{endpoint}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_page(endpoint: str, offset: int, filters: str | None) -> dict:
    extra = {"filters": filters} if filters else {}
    return _api(endpoint, limit=PAGE_SIZE, offset=offset, **extra)


def _partition_filters(endpoint: str) -> list[str | None]:
    """Return the list of `filters` values to page over for this endpoint.

    A single-element [None] means page the whole endpoint with no filter.
    Partitioned endpoints discover their partition values from the source
    (no hardcoded ranges)."""
    field = PARTITION_FIELD.get(endpoint)
    if field is None:
        return [None]
    if field == "YEAR":
        lo = int(_api(endpoint, limit=1, sort_by="YEAR", sort_order="ASC",
                      fields="YEAR")["data"][0]["data"]["YEAR"])
        hi = int(_api(endpoint, limit=1, sort_by="YEAR", sort_order="DESC",
                      fields="YEAR")["data"][0]["data"]["YEAR"])
        return [f"YEAR:{y}" for y in range(lo, hi + 1)]
    raise RuntimeError(f"unknown partition field {field!r} for {endpoint}")


# ---- coercion ----------------------------------------------------------

def _coerce_str(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _coerce_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _project(rows, cols: dict[str, str]) -> dict[str, list]:
    """Return a column-oriented dict for one page, coercing each value."""
    out = {c: [] for c in cols}
    for item in rows:
        rec = item.get("data", {})
        for c, t in cols.items():
            v = rec.get(c)
            out[c].append(_coerce_str(v) if t == "s" else _coerce_float(v))
    return out


# ---- download ----------------------------------------------------------

def _page_partition(endpoint, filters, cols, schema, writer) -> int:
    """Page one partition fully into the writer; return rows written."""
    first = _fetch_page(endpoint, 0, filters)
    total = int(first.get("meta", {}).get("total", 0))
    if total > RESULT_WINDOW:
        raise RuntimeError(
            f"{endpoint} partition {filters!r}: total={total} exceeds the "
            f"{RESULT_WINDOW} result window — needs finer partitioning"
        )
    if total == 0:
        return 0

    written = 0
    offset = 0
    payload = first
    for page in range(MAX_PAGES + 1):
        if page >= MAX_PAGES:
            raise RuntimeError(
                f"{endpoint} partition {filters!r}: hit MAX_PAGES={MAX_PAGES}"
            )
        rows = payload.get("data") or []
        if not rows:
            break
        writer.write_table(pa.table(_project(rows, cols), schema=schema))
        written += len(rows)
        offset += PAGE_SIZE
        if offset >= total:
            break
        payload = _fetch_page(endpoint, offset, filters)

    if written != total:
        raise RuntimeError(
            f"{endpoint} partition {filters!r}: wrote {written} rows but "
            f"meta.total={total} — pagination terminated early"
        )
    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    endpoint = node_id[len("fdic-"):]
    cols = COLUMNS[endpoint]
    schema = pa.schema([(c, _PA_TYPE[t]) for c, t in cols.items()])

    total_written = 0
    with raw_parquet_writer(asset, schema) as writer:
        for filters in _partition_filters(endpoint):
            total_written += _page_partition(
                endpoint, filters, cols, schema, writer
            )
    print(f"  [fdic] {node_id}: {total_written:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"fdic-{eid}", fn=fetch_one, kind="download")
    for eid in COLUMNS
]


# ---- transform: one published Delta table per endpoint -----------------
# Raw parquet is already curated and typed, so each transform is a thin
# pass-through publish. Dep view is named after the download id.

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
