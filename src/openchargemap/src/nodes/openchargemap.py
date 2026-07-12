"""Open Charge Map downloads.

Source: the official keyless bulk export of the live Open Charge Map registry
(GitHub repo openchargemap/ocm-export, default branch 'main').
"""

import io
import json
import re
import tarfile

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

EXPORT_TARBALL_URL = "https://codeload.github.com/openchargemap/ocm-export/tar.gz/refs/heads/main"
REFERENCEDATA_URL = "https://raw.githubusercontent.com/openchargemap/ocm-export/main/data/referencedata.json"

_COUNTRY_DIR_RE = re.compile(r"^[A-Z]{2}$")
_PREFIX = "openchargemap-"


def _schema(*fields: tuple[str, pa.DataType]) -> pa.Schema:
    return pa.schema(list(fields))


POIS_SCHEMA = _schema(
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
)

REFERENCE_CONFIGS = {
    "chargertypes": {
        "source_key": "ChargerTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("comments", pa.string()),
            ("is_fast_charge_capable", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "comments": r.get("Comments"),
            "is_fast_charge_capable": _as_bool(r.get("IsFastChargeCapable")),
        },
    },
    "checkinstatustypes": {
        "source_key": "CheckinStatusTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("is_automated_checkin", pa.bool_()),
            ("is_positive", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "is_automated_checkin": _as_bool(r.get("IsAutomatedCheckin")),
            "is_positive": _as_bool(r.get("IsPositive")),
        },
    },
    "connectiontypes": {
        "source_key": "ConnectionTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("formal_name", pa.string()),
            ("is_discontinued", pa.bool_()),
            ("is_obsolete", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "formal_name": r.get("FormalName"),
            "is_discontinued": _as_bool(r.get("IsDiscontinued")),
            "is_obsolete": _as_bool(r.get("IsObsolete")),
        },
    },
    "countries": {
        "source_key": "Countries",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("iso_code", pa.string()),
            ("continent_code", pa.string()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "iso_code": r.get("ISOCode"),
            "continent_code": r.get("ContinentCode"),
        },
    },
    "currenttypes": {
        "source_key": "CurrentTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("description", pa.string()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "description": r.get("Description"),
        },
    },
    "dataproviders": {
        "source_key": "DataProviders",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("website_url", pa.string()),
            ("comments", pa.string()),
            ("status_type_id", pa.int64()),
            ("status_type_title", pa.string()),
            ("is_provider_enabled", pa.bool_()),
            ("is_restricted_edit", pa.bool_()),
            ("is_open_data_licensed", pa.bool_()),
            ("is_approved_import", pa.bool_()),
            ("license", pa.string()),
            ("date_last_imported", pa.string()),
        ),
        "row": lambda r: _data_provider_row(r),
    },
    "datatypes": {
        "source_key": "DataTypes",
        "schema": _schema(("id", pa.int64()), ("title", pa.string())),
        "row": lambda r: {"id": _as_int(r.get("ID")), "title": r.get("Title")},
    },
    "metadatagroups": {
        "source_key": "MetadataGroups",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("data_provider_id", pa.int64()),
            ("is_restricted_edit", pa.bool_()),
            ("is_public_interest", pa.bool_()),
            ("metadata_fields_json", pa.string()),
            ("metadata_field_count", pa.int64()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "data_provider_id": _as_int(r.get("DataProviderID")),
            "is_restricted_edit": _as_bool(r.get("IsRestrictedEdit")),
            "is_public_interest": _as_bool(r.get("IsPublicInterest")),
            "metadata_fields_json": _json_text(r.get("MetadataFields")),
            "metadata_field_count": len(r.get("MetadataFields") or []),
        },
    },
    "operators": {
        "source_key": "Operators",
        "schema": _schema(
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
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "website_url": r.get("WebsiteURL"),
            "comments": r.get("Comments"),
            "contact_email": r.get("ContactEmail"),
            "fault_report_email": r.get("FaultReportEmail"),
            "phone_primary": r.get("PhonePrimaryContact"),
            "phone_secondary": r.get("PhoneSecondaryContact"),
            "booking_url": r.get("BookingURL"),
            "is_private_individual": _as_bool(r.get("IsPrivateIndividual")),
            "is_restricted_edit": _as_bool(r.get("IsRestrictedEdit")),
        },
    },
    "statustypes": {
        "source_key": "StatusTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("is_operational", pa.bool_()),
            ("is_user_selectable", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "is_operational": _as_bool(r.get("IsOperational")),
            "is_user_selectable": _as_bool(r.get("IsUserSelectable")),
        },
    },
    "submissionstatustypes": {
        "source_key": "SubmissionStatusTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("is_live", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "is_live": _as_bool(r.get("IsLive")),
        },
    },
    "usagetypes": {
        "source_key": "UsageTypes",
        "schema": _schema(
            ("id", pa.int64()),
            ("title", pa.string()),
            ("is_pay_at_location", pa.bool_()),
            ("is_membership_required", pa.bool_()),
            ("is_access_key_required", pa.bool_()),
        ),
        "row": lambda r: {
            "id": _as_int(r.get("ID")),
            "title": r.get("Title"),
            "is_pay_at_location": _as_bool(r.get("IsPayAtLocation")),
            "is_membership_required": _as_bool(r.get("IsMembershipRequired")),
            "is_access_key_required": _as_bool(r.get("IsAccessKeyRequired")),
        },
    },
    "usercommenttypes": {
        "source_key": "UserCommentTypes",
        "schema": _schema(("id", pa.int64()), ("title", pa.string())),
        "row": lambda r: {"id": _as_int(r.get("ID")), "title": r.get("Title")},
    },
}


def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


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


def _as_bool(v):
    return v if isinstance(v, bool) else None


def _json_text(value) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _data_provider_row(r: dict) -> dict:
    status = r.get("DataProviderStatusType") or {}
    return {
        "id": _as_int(r.get("ID")),
        "title": r.get("Title"),
        "website_url": r.get("WebsiteURL"),
        "comments": r.get("Comments"),
        "status_type_id": _as_int(status.get("ID")),
        "status_type_title": status.get("Title"),
        "is_provider_enabled": _as_bool(status.get("IsProviderEnabled")),
        "is_restricted_edit": _as_bool(r.get("IsRestrictedEdit")),
        "is_open_data_licensed": _as_bool(r.get("IsOpenDataLicensed")),
        "is_approved_import": _as_bool(r.get("IsApprovedImport")),
        "license": r.get("License"),
        "date_last_imported": r.get("DateLastImported"),
    }


def _summarise_connections(connections):
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
        **_summarise_connections(poi.get("Connections")),
    }


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(_PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id.removeprefix(_PREFIX)


def fetch_pois(node_id: str) -> None:
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
            if len(rest) != 2 or not _COUNTRY_DIR_RE.match(rest[0]) or not rest[1].endswith(".json"):
                continue
            fh = tf.extractfile(member)
            if fh is None:
                continue
            rows.append(_poi_to_row(json.loads(fh.read()), rest[0]))

    if not rows:
        raise AssertionError("OCM export tarball yielded 0 POI rows; layout changed")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=POIS_SCHEMA), node_id)


def fetch_reference(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    config = REFERENCE_CONFIGS.get(entity_id)
    if config is None:
        raise ValueError(f"no reference config for {entity_id!r}")

    ref = _get_json(REFERENCEDATA_URL)
    source_key = config["source_key"]
    source_rows = ref.get(source_key) or []
    rows = [config["row"](row) for row in source_rows]
    if not rows:
        raise AssertionError(f"referencedata.json had no {source_key} rows; layout changed")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=config["schema"]), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openchargemap-chargertypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-checkinstatustypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-connectiontypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-countries", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-currenttypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-dataproviders", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-datatypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-metadatagroups", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-operators", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-pois", fn=fetch_pois, kind="download"),
    NodeSpec(id="openchargemap-statustypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-submissionstatustypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-usagetypes", fn=fetch_reference, kind="download"),
    NodeSpec(id="openchargemap-usercommenttypes", fn=fetch_reference, kind="download"),
]
