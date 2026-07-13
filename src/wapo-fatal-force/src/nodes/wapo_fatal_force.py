from __future__ import annotations

import csv
from datetime import date
from io import StringIO

import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)


BASE_URL = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/v2"
DEATH_RECORDS_URL = f"{BASE_URL}/fatal-police-shootings-data.csv"
AGENCIES_URL = f"{BASE_URL}/fatal-police-shootings-agencies.csv"


DEATH_RECORDS_SCHEMA = pa.schema(
    [
        ("id", pa.int64()),
        ("date", pa.date32()),
        ("threat_type", pa.string()),
        ("flee_status", pa.string()),
        ("armed_with", pa.string()),
        ("city", pa.string()),
        ("county", pa.string()),
        ("state", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("location_precision", pa.string()),
        ("name", pa.string()),
        ("age", pa.int64()),
        ("gender", pa.string()),
        ("race", pa.string()),
        ("race_source", pa.string()),
        ("was_mental_illness_related", pa.bool_()),
        ("body_camera", pa.bool_()),
        ("agency_ids", pa.string()),
    ]
)

AGENCIES_SCHEMA = pa.schema(
    [
        ("id", pa.int64()),
        ("name", pa.string()),
        ("type", pa.string()),
        ("state", pa.string()),
        ("oricodes", pa.string()),
        ("total_shootings", pa.int64()),
    ]
)


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _int(value: str | None) -> int | None:
    value = _clean(value)
    return int(value) if value is not None else None


def _float(value: str | None) -> float | None:
    value = _clean(value)
    return float(value) if value is not None else None


def _bool(value: str | None) -> bool | None:
    value = _clean(value)
    if value is None:
        return None
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"unexpected boolean literal: {value!r}")


def _date(value: str | None) -> date | None:
    value = _clean(value)
    return date.fromisoformat(value) if value is not None else None


def _read_csv(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(StringIO(text)))


def _fetch_text(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp, resp.content.decode("utf-8-sig")


def fetch_death_records(node_id: str) -> None:
    resp, text = _fetch_text(DEATH_RECORDS_URL)
    rows = []
    for row in _read_csv(text):
        rows.append(
            {
                "id": _int(row.get("id")),
                "date": _date(row.get("date")),
                "threat_type": _clean(row.get("threat_type")),
                "flee_status": _clean(row.get("flee_status")),
                "armed_with": _clean(row.get("armed_with")),
                "city": _clean(row.get("city")),
                "county": _clean(row.get("county")),
                "state": _clean(row.get("state")),
                "latitude": _float(row.get("latitude")),
                "longitude": _float(row.get("longitude")),
                "location_precision": _clean(row.get("location_precision")),
                "name": _clean(row.get("name")),
                "age": _int(row.get("age")),
                "gender": _clean(row.get("gender")),
                "race": _clean(row.get("race")),
                "race_source": _clean(row.get("race_source")),
                "was_mental_illness_related": _bool(row.get("was_mental_illness_related")),
                "body_camera": _bool(row.get("body_camera")),
                "agency_ids": _clean(row.get("agency_ids")),
            }
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=DEATH_RECORDS_SCHEMA), node_id)
    record_source_signature(node_id, DEATH_RECORDS_URL, response=resp)


def fetch_agencies(node_id: str) -> None:
    resp, text = _fetch_text(AGENCIES_URL)
    rows = []
    for row in _read_csv(text):
        rows.append(
            {
                "id": _int(row.get("id")),
                "name": _clean(row.get("name")),
                "type": _clean(row.get("type")),
                "state": _clean(row.get("state")),
                "oricodes": _clean(row.get("oricodes")),
                "total_shootings": _int(row.get("total_shootings")),
            }
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=AGENCIES_SCHEMA), node_id)
    record_source_signature(node_id, AGENCIES_URL, response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="wapo-fatal-force-fatal-police-shootings",
        fn=fetch_death_records,
    ),
    NodeSpec(
        id="wapo-fatal-force-fatal-police-shootings-agencies",
        fn=fetch_agencies,
    ),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="wapo-fatal-force-fatal-police-shootings",
        description=(
            "Washington Post says the GitHub Fatal Force database is updated regularly; "
            "skip only when raw.githubusercontent.com ETag/Last-Modified is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, DEATH_RECORDS_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id="wapo-fatal-force-fatal-police-shootings-agencies",
        description=(
            "Washington Post says the GitHub Fatal Force database is updated regularly; "
            "skip only when raw.githubusercontent.com ETag/Last-Modified is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, AGENCIES_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
]
