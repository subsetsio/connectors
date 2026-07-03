"""Open Charge Map connector.

Source: the official keyless bulk export of the live Open Charge Map registry
(GitHub repo openchargemap/ocm-export, default branch 'main'). Two subsets:

  * openchargemap-pois       one row per EV charging location (POI). Built from
                             the per-POI JSON files in the export tarball — a
                             single ~23MB gzip holding the whole global corpus
                             (~129k POIs across 126 country folders). Connections
                             (the per-plug array) are summarised onto each POI
                             row (count / total quantity / max power / plug-type
                             id set) so the grain stays one-row-per-location.
  * openchargemap-operators  the charging-network operator directory, parsed from
                             data/referencedata.json in the same export.

Stateless full re-pull each run (shape 1): the whole corpus is a single small
tarball, so we re-fetch and overwrite every refresh — revisions and removals are
picked up for free. The underlying live REST API supports modifiedsince/cursor
filtering but requires a registered API key for all calls; the keyless GitHub
export is used instead (see research download_handoff).
"""

import io
import re
import tarfile

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)

EXPORT_TARBALL_URL = "https://codeload.github.com/openchargemap/ocm-export/tar.gz/refs/heads/main"
REFERENCEDATA_URL = "https://raw.githubusercontent.com/openchargemap/ocm-export/main/data/referencedata.json"

# tarball member path looks like: ocm-export-<sha>/data/<ISO2>/OCM-<id>.json
_COUNTRY_DIR_RE = re.compile(r"^[A-Z]{2}$")

POIS_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("uuid", pa.string()),
    ("country_code", pa.string()),
    ("country_id", pa.int64()),
    ("data_provider_id", pa.int64()),
    ("operator_id", pa.int64()),
    ("usage_type_id", pa.int64()),
    ("status_type_id", pa.int64()),
    ("submission_status_type_id", pa.int64()),
    ("usage_cost", pa.string()),
    ("number_of_points", pa.int64()),
    ("title", pa.string()),
    ("address_line1", pa.string()),
    ("town", pa.string()),
    ("state_or_province", pa.string()),
    ("postcode", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("num_connections", pa.int64()),
    ("total_quantity", pa.int64()),
    ("max_power_kw", pa.float64()),
    ("connection_type_ids", pa.string()),
    ("date_created", pa.string()),
    ("date_last_verified", pa.string()),
    ("date_last_status_update", pa.string()),
])

OPERATORS_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("title", pa.string()),
    ("website_url", pa.string()),
    ("comments", pa.string()),
    ("contact_email", pa.string()),
    ("fault_report_email", pa.string()),
    ("phone_primary", pa.string()),
    ("phone_secondary", pa.string()),
    ("booking_url", pa.string()),
    ("is_private_individual", pa.bool_()),
    ("is_restricted_edit", pa.bool_()),
])


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _as_int(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _as_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _summarise_connections(connections):
    """Collapse a POI's Connections[] array into per-location summary fields."""
    n = 0
    total_qty = 0
    saw_qty = False
    max_power = None
    type_ids = set()
    for c in connections or []:
        n += 1
        q = _as_int(c.get("Quantity"))
        if q is not None:
            total_qty += q
            saw_qty = True
        p = _as_float(c.get("PowerKW"))
        if p is not None and (max_power is None or p > max_power):
            max_power = p
        tid = _as_int(c.get("ConnectionTypeID"))
        if tid is not None:
            type_ids.add(tid)
    return {
        "num_connections": n,
        "total_quantity": total_qty if saw_qty else None,
        "max_power_kw": max_power,
        "connection_type_ids": ",".join(str(t) for t in sorted(type_ids)) or None,
    }


def _poi_to_row(poi: dict, country_code: str) -> dict:
    addr = poi.get("AddressInfo") or {}
    conn = _summarise_connections(poi.get("Connections"))
    return {
        "id": _as_int(poi.get("ID")),
        "uuid": poi.get("UUID"),
        "country_code": country_code,
        "country_id": _as_int(addr.get("CountryID")),
        "data_provider_id": _as_int(poi.get("DataProviderID")),
        "operator_id": _as_int(poi.get("OperatorID")),
        "usage_type_id": _as_int(poi.get("UsageTypeID")),
        "status_type_id": _as_int(poi.get("StatusTypeID")),
        "submission_status_type_id": _as_int(poi.get("SubmissionStatusTypeID")),
        "usage_cost": poi.get("UsageCost"),
        "number_of_points": _as_int(poi.get("NumberOfPoints")),
        "title": addr.get("Title"),
        "address_line1": addr.get("AddressLine1"),
        "town": addr.get("Town"),
        "state_or_province": addr.get("StateOrProvince"),
        "postcode": addr.get("Postcode"),
        "latitude": _as_float(addr.get("Latitude")),
        "longitude": _as_float(addr.get("Longitude")),
        "date_created": poi.get("DateCreated"),
        "date_last_verified": poi.get("DateLastVerified"),
        "date_last_status_update": poi.get("DateLastStatusUpdate"),
        **conn,
    }


def fetch_pois(node_id: str) -> None:
    import json

    asset = node_id
    raw = _get_bytes(EXPORT_TARBALL_URL)
    rows = []
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        for member in tf:
            if not member.isfile():
                continue
            parts = member.name.split("/")
            if "data" not in parts:
                continue
            rest = parts[parts.index("data") + 1:]
            # want data/<ISO2>/OCM-<id>.json (skip data/referencedata.json)
            if len(rest) != 2 or not _COUNTRY_DIR_RE.match(rest[0]) or not rest[1].endswith(".json"):
                continue
            fh = tf.extractfile(member)
            if fh is None:
                continue
            poi = json.loads(fh.read())
            rows.append(_poi_to_row(poi, rest[0]))

    if not rows:
        raise AssertionError("OCM export tarball yielded 0 POI rows — layout changed?")

    table = pa.Table.from_pylist(rows, schema=POIS_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_operators(node_id: str) -> None:
    asset = node_id
    ref = _get_json(REFERENCEDATA_URL)
    operators = ref.get("Operators") or []
    rows = [
        {
            "id": _as_int(o.get("ID")),
            "title": o.get("Title"),
            "website_url": o.get("WebsiteURL"),
            "comments": o.get("Comments"),
            "contact_email": o.get("ContactEmail"),
            "fault_report_email": o.get("FaultReportEmail"),
            "phone_primary": o.get("PhonePrimaryContact"),
            "phone_secondary": o.get("PhoneSecondaryContact"),
            "booking_url": o.get("BookingURL"),
            "is_private_individual": o.get("IsPrivateIndividual"),
            "is_restricted_edit": o.get("IsRestrictedEdit"),
        }
        for o in operators
    ]
    if not rows:
        raise AssertionError("referencedata.json had no Operators — layout changed?")

    table = pa.Table.from_pylist(rows, schema=OPERATORS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="openchargemap-pois", fn=fetch_pois, kind="download"),
    NodeSpec(id="openchargemap-operators", fn=fetch_operators, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openchargemap-pois-transform",
        deps=["openchargemap-pois"],
        key=("id",),
        temporal="date_last_verified",
        sql='''
            SELECT
                id,
                uuid,
                country_code,
                country_id,
                data_provider_id,
                operator_id,
                usage_type_id,
                status_type_id,
                submission_status_type_id,
                usage_cost,
                number_of_points,
                title,
                address_line1,
                town,
                state_or_province,
                postcode,
                latitude,
                longitude,
                num_connections,
                total_quantity,
                max_power_kw,
                connection_type_ids,
                try_cast(date_created AS TIMESTAMP)            AS date_created,
                try_cast(date_last_verified AS TIMESTAMP)      AS date_last_verified,
                try_cast(date_last_status_update AS TIMESTAMP) AS date_last_status_update
            FROM "openchargemap-pois"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="openchargemap-operators-transform",
        deps=["openchargemap-operators"],
        key=("id",),
        sql='''
            SELECT
                id,
                title,
                website_url,
                comments,
                contact_email,
                fault_report_email,
                phone_primary,
                phone_secondary,
                booking_url,
                is_private_individual,
                is_restricted_edit
            FROM "openchargemap-operators"
            WHERE id IS NOT NULL
        ''',
    ),
]
