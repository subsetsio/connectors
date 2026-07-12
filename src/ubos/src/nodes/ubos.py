import csv
import io
import json
import zipfile

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

BASE_URL = "https://ons-sdg-ug-ubos.github.io/data/en"
META_URL = f"{BASE_URL}/meta/all.json"
ZIP_URL = f"{BASE_URL}/zip/all_indicators.zip"

INDICATORS_SCHEMA = pa.schema(
    [
        ("indicator_id", pa.string()),
        ("indicator_name", pa.string()),
        ("graph_title", pa.string()),
        ("reporting_status", pa.string()),
        ("sdg_goal", pa.string()),
        ("sdg_target", pa.string()),
        ("sdg_indicator", pa.string()),
        ("unit_measure", pa.string()),
        ("source_type", pa.string()),
        ("meta_last_update", pa.string()),
        ("copyright", pa.string()),
        ("raw_metadata_json", pa.string()),
    ]
)

VALUES_SCHEMA = pa.schema(
    [
        ("indicator_id", pa.string()),
        ("year", pa.int16()),
        ("value", pa.float64()),
        ("observation_status", pa.string()),
        ("unit_multiplier", pa.string()),
        ("source_details", pa.string()),
        ("series", pa.string()),
        ("reference_area", pa.string()),
        ("unit_measure", pa.string()),
        ("age", pa.string()),
        ("composite_breakdown", pa.string()),
        ("degree_of_urbanisation", pa.string()),
        ("disability_status", pa.string()),
        ("education_level", pa.string()),
        ("occupation", pa.string()),
        ("sex", pa.string()),
        ("time_period_details", pa.string()),
        ("type_of_product", pa.string()),
    ]
)

CSV_FIELD_MAP = {
    "Age": "age",
    "COMPOSITE_BREAKDOWN": "composite_breakdown",
    "Degree of urbanisation": "degree_of_urbanisation",
    "Disability status": "disability_status",
    "Education level": "education_level",
    "Observation status": "observation_status",
    "Occupation": "occupation",
    "Reference area": "reference_area",
    "SERIES": "series",
    "Sex": "sex",
    "Source details": "source_details",
    "Time period details": "time_period_details",
    "Type of product": "type_of_product",
    "UNIT_MEASURE": "unit_measure",
    "Unit multiplier": "unit_multiplier",
}


def _none_if_blank(value):
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _to_year(value):
    value = _none_if_blank(value)
    if value is None:
        return None
    try:
        return int(float(value))
    except ValueError as exc:
        raise ValueError(f"invalid Year value {value!r}") from exc


def _to_float(value):
    value = _none_if_blank(value)
    if value is None:
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError as exc:
        raise ValueError(f"invalid Value value {value!r}") from exc


def _table(rows, schema):
    return pa.Table.from_pylist(rows, schema=schema)


def fetch_indicators(node_id: str) -> None:
    resp = get(META_URL, timeout=(10.0, 180.0))
    resp.raise_for_status()
    meta = resp.json()
    if not isinstance(meta, dict):
        raise TypeError("meta/all.json must be an object keyed by indicator id")

    rows = []
    for indicator_id, record in sorted(meta.items()):
        if not isinstance(record, dict):
            raise TypeError(f"{indicator_id}: metadata record is not an object")
        rows.append(
            {
                "indicator_id": indicator_id,
                "indicator_name": _none_if_blank(record.get("indicator_name")),
                "graph_title": _none_if_blank(record.get("graph_title")),
                "reporting_status": _none_if_blank(record.get("reporting_status")),
                "sdg_goal": _none_if_blank(record.get("SDG_GOAL") or record.get("sdg_goal")),
                "sdg_target": _none_if_blank(record.get("SDG_TARGET") or record.get("sdg_target")),
                "sdg_indicator": _none_if_blank(record.get("SDG_INDICATOR") or record.get("sdg_indicator")),
                "unit_measure": _none_if_blank(record.get("UNIT_MEASURE") or record.get("unit_measure")),
                "source_type": _none_if_blank(record.get("SOURCE_TYPE") or record.get("source_type")),
                "meta_last_update": _none_if_blank(
                    record.get("META_LAST_UPDATE") or record.get("meta_last_update")
                ),
                "copyright": _none_if_blank(record.get("copyright")),
                "raw_metadata_json": json.dumps(record, sort_keys=True, separators=(",", ":")),
            }
        )

    if len(rows) < 200:
        raise AssertionError(f"{node_id}: expected at least 200 indicator records, got {len(rows)}")
    save_raw_parquet(_table(rows, INDICATORS_SCHEMA), node_id)
    record_source_signature(node_id, META_URL, response=resp)


def fetch_values(node_id: str) -> None:
    resp = get(ZIP_URL, timeout=(10.0, 180.0))
    resp.raise_for_status()

    rows = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as archive:
        csv_names = sorted(name for name in archive.namelist() if name.endswith(".csv"))
        if len(csv_names) < 100:
            raise AssertionError(f"{node_id}: expected at least 100 indicator CSVs, got {len(csv_names)}")
        for name in csv_names:
            indicator_id = name.rsplit("/", 1)[-1].removesuffix(".csv")
            with archive.open(name) as raw:
                text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
                reader = csv.DictReader(text)
                for row in reader:
                    out = {
                        "indicator_id": indicator_id,
                        "year": _to_year(row.get("Year")),
                        "value": _to_float(row.get("Value")),
                    }
                    for source_name, target_name in CSV_FIELD_MAP.items():
                        out[target_name] = _none_if_blank(row.get(source_name))
                    rows.append(out)

    if len(rows) < 2000:
        raise AssertionError(f"{node_id}: expected at least 2000 observation rows, got {len(rows)}")
    save_raw_parquet(_table(rows, VALUES_SCHEMA), node_id)
    record_source_signature(node_id, ZIP_URL, response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(id="ubos-indicators", fn=fetch_indicators),
    NodeSpec(id="ubos-values", fn=fetch_values),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="ubos-indicators",
        description="Static Open SDG metadata; refreshed weekly or when GitHub Pages validators change.",
        check=lambda aid: source_unchanged(aid, META_URL) and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id="ubos-values",
        description="Static Open SDG all_indicators.zip; refreshed weekly or when GitHub Pages validators change.",
        check=lambda aid: source_unchanged(aid, ZIP_URL) and raw_asset_exists(aid, "parquet"),
    ),
]
