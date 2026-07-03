"""APNIC connector.

Three independent statistical products from APNIC (the Asia-Pacific Regional
Internet Registry), each a single published Delta table:

- apnic-delegated-resources : the RIR "extended" delegated-stats bulk file
  (one row per allocated/assigned Internet number resource). A daily full
  snapshot — stateless full re-pull.
- apnic-ipv6-capability     : APNIC Labs IPv6 capability measurement, the
  per-economy daily time series (one row per economy-date). Built by unioning
  the per-economy JSON files (v6economy/<ISO2>.json). The economy code set is
  discovered at fetch time from the aspop endpoint (no hardcoded country list).
  Full corpus per refresh — each file is a complete daily history.
- apnic-as-user-population  : APNIC Labs per-AS end-user population estimates
  (one row per AS for the current measurement window). Single global JSON.

All three are stateless full re-pulls: APNIC exposes no incremental/`since`
filter, every artefact is a complete snapshot/history fetched in one go, and the
volumes are small (low tens of MB). Freshness gating is the maintain step's job.
"""

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

DELEGATED_URL = "https://ftp.apnic.net/stats/apnic/delegated-apnic-extended-latest"
ASPOP_URL = "https://stats.labs.apnic.net/cgi-bin/aspop?f=j"
V6ECONOMY_URL = "https://data1.labs.apnic.net/v6stats/v6economy/{cc}.json"


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------
# 1. Delegated resources
# --------------------------------------------------------------------------

_DELEGATED_SCHEMA = pa.schema([
    ("registry", pa.string()),
    ("cc", pa.string()),
    ("resource_type", pa.string()),
    ("start", pa.string()),
    ("value", pa.int64()),
    ("date", pa.string()),
    ("status", pa.string()),
    ("opaque_id", pa.string()),
])


def fetch_delegated_resources(node_id: str) -> None:
    asset = node_id
    text = _get_text(DELEGATED_URL)
    rows = []
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        # Records carry a real resource type; this skips the version header
        # (type field is a date) and the per-type summary lines (field[5]).
        if len(p) < 7 or p[2] not in ("asn", "ipv4", "ipv6"):
            continue
        if len(p) >= 6 and p[5] == "summary":
            continue
        try:
            value = int(p[4])
        except ValueError:
            value = None
        rows.append({
            "registry": p[0],
            "cc": p[1] or None,
            "resource_type": p[2],
            "start": p[3] or None,
            "value": value,
            "date": p[5] or None,
            "status": p[6],
            "opaque_id": p[7] if len(p) > 7 and p[7] else None,
        })
    table = pa.Table.from_pylist(rows, schema=_DELEGATED_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------
# 2. IPv6 capability (per-economy time series)
# --------------------------------------------------------------------------

_IPV6_SCHEMA = pa.schema([
    ("economy", pa.string()),
    ("date", pa.string()),
    ("seen", pa.float64()),
    ("preferred", pa.float64()),
    ("capable", pa.float64()),
    ("preferred_pc", pa.float64()),
    ("capable_pc", pa.float64()),
    ("preferred_pc_30d", pa.float64()),
    ("capable_pc_30d", pa.float64()),
])


def _economy_codes() -> list[str]:
    """Discover the set of economy codes APNIC measures, from the aspop
    dataset's CC column. Avoids hardcoding an ISO-3166 list and tracks APNIC's
    actual coverage."""
    pop = _get_json(ASPOP_URL)
    codes = {row["CC"] for row in pop.get("Data", []) if row.get("CC")}
    return sorted(codes)


def _ipv6_rows_for_economy(cc: str):
    """Fetch and flatten one economy's IPv6 time series. Returns [] if APNIC
    has no measurement file for this economy (permanent 404)."""
    import httpx
    try:
        doc = _get_json(V6ECONOMY_URL.format(cc=cc))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return []
        raise
    out = []
    for rec in doc.get("data", []):
        raw = rec.get("raw") or {}
        d30 = rec.get("30") or {}
        out.append({
            "economy": rec.get("cc") or cc,
            "date": rec.get("date"),
            "seen": raw.get("seen"),
            "preferred": raw.get("preferred"),
            "capable": raw.get("capable"),
            "preferred_pc": raw.get("preferred_pc"),
            "capable_pc": raw.get("capable_pc"),
            "preferred_pc_30d": d30.get("preferred_pc"),
            "capable_pc_30d": d30.get("capable_pc"),
        })
    return out


def fetch_ipv6_capability(node_id: str) -> None:
    asset = node_id
    rows = []
    for cc in _economy_codes():
        rows.extend(_ipv6_rows_for_economy(cc))
    table = pa.Table.from_pylist(rows, schema=_IPV6_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------
# 3. Per-AS end-user population estimates
# --------------------------------------------------------------------------

_ASPOP_SCHEMA = pa.schema([
    ("rank", pa.int64()),
    ("asn", pa.int64()),
    ("description", pa.string()),
    ("cc", pa.string()),
    ("users", pa.int64()),
    ("pct_cc_pop", pa.float64()),
    ("pct_internet", pa.float64()),
    ("samples", pa.int64()),
])


def fetch_as_user_population(node_id: str) -> None:
    asset = node_id
    pop = _get_json(ASPOP_URL)
    rows = []
    for r in pop.get("Data", []):
        rows.append({
            "rank": r.get("rank"),
            "asn": r.get("AS"),
            "description": r.get("Description"),
            "cc": r.get("CC"),
            "users": r.get("Users"),
            "pct_cc_pop": r.get("Percent of CC Pop"),
            "pct_internet": r.get("Percent of Internet"),
            "samples": r.get("Samples"),
        })
    table = pa.Table.from_pylist(rows, schema=_ASPOP_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------
# DAG
# --------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="apnic-delegated-resources", fn=fetch_delegated_resources, kind="download"),
    NodeSpec(id="apnic-ipv6-capability", fn=fetch_ipv6_capability, kind="download"),
    NodeSpec(id="apnic-as-user-population", fn=fetch_as_user_population, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="apnic-delegated-resources-transform",
        deps=["apnic-delegated-resources"],
        sql='''
            SELECT
                registry,
                cc                                                         AS economy,
                resource_type,
                "start"                                                    AS resource_start,
                "value",
                TRY_CAST(STRPTIME(NULLIF("date", '00000000'), '%Y%m%d') AS DATE) AS allocation_date,
                status,
                opaque_id
            FROM "apnic-delegated-resources"
        ''',
        temporal="allocation_date",
    ),
    SqlNodeSpec(
        id="apnic-ipv6-capability-transform",
        deps=["apnic-ipv6-capability"],
        sql='''
            SELECT
                CAST("date" AS DATE) AS date,
                economy,
                seen,
                preferred,
                capable,
                preferred_pc,
                capable_pc,
                preferred_pc_30d,
                capable_pc_30d
            FROM "apnic-ipv6-capability"
            WHERE "date" IS NOT NULL AND seen IS NOT NULL
        ''',
        key=("economy", "date"),
        temporal="date",
    ),
    SqlNodeSpec(
        id="apnic-as-user-population-transform",
        deps=["apnic-as-user-population"],
        sql='''
            SELECT
                rank,
                asn,
                description,
                cc AS economy,
                users,
                pct_cc_pop,
                pct_internet,
                samples
            FROM "apnic-as-user-population"
            WHERE asn IS NOT NULL
        ''',
        key=("asn",),
    ),
]
