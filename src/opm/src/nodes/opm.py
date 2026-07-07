from __future__ import annotations

import io
import os

import pyarrow as pa
import pyarrow.parquet as pq
from subsets_utils import NodeSpec, get, list_raw_fragments, save_raw_parquet


BASE_URL = "https://data.opm.gov/api/v1"
FAMILIES = ("accessions", "employment", "separations")

STRING_COLUMNS = (
    "accession_category",
    "accession_category_code",
    "age_bracket",
    "agency",
    "agency_code",
    "agency_subelement",
    "agency_subelement_code",
    "annualized_adjusted_basic_pay",
    "appointment_not_to_exceed_date",
    "appointment_type",
    "appointment_type_code",
    "bargaining_unit",
    "bargaining_unit_code",
    "bargaining_unit_status",
    "cfo_act_agency_indicator",
    "consolidated_statistical_area",
    "consolidated_statistical_area_code",
    "core_based_statistical_area",
    "core_based_statistical_area_code",
    "count",
    "department",
    "department_code",
    "drp_indicator",
    "duty_station_city",
    "duty_station_code",
    "duty_station_country",
    "duty_station_country_code",
    "duty_station_county",
    "duty_station_county_code",
    "duty_station_state",
    "duty_station_state_abbreviation",
    "duty_station_state_code",
    "duty_station_state_country_territory_code",
    "education_level",
    "education_level_bracket",
    "education_level_code",
    "flsa_category",
    "flsa_category_code",
    "grade",
    "length_of_service_years",
    "locality_pay_area",
    "locality_pay_area_code",
    "nsftp_indicator",
    "occupational_category",
    "occupational_category_code",
    "occupational_group",
    "occupational_group_code",
    "occupational_series",
    "occupational_series_code",
    "pathways_group",
    "pay_basis",
    "pay_basis_code",
    "pay_plan",
    "pay_plan_code",
    "personnel_action_effective_date_yyyymm",
    "personnel_office_identifier_code",
    "position_occupied",
    "position_occupied_code",
    "service_computation_date_leave",
    "separation_category",
    "separation_category_code",
    "snapshot_yyyymm",
    "stem_occupation",
    "stem_occupation_type",
    "step_or_rate_type",
    "step_or_rate_type_code",
    "supervisory_status",
    "supervisory_status_code",
    "tenure",
    "tenure_code",
    "veteran_indicator",
    "work_schedule",
    "work_schedule_code",
)

SCHEMA = pa.schema(
    [pa.field(col, pa.string()) for col in STRING_COLUMNS]
    + [
        pa.field("source_family", pa.string()),
        pa.field("source_filename", pa.string()),
        pa.field("source_publish_date", pa.string()),
        pa.field("source_year", pa.int16()),
        pa.field("source_month", pa.int8()),
        pa.field("source_version", pa.int16()),
    ]
)


def _family_from_node_id(node_id: str) -> str:
    family = node_id.removeprefix("opm-")
    if family not in FAMILIES:
        raise ValueError(f"Unsupported OPM node id: {node_id}")
    return family


def _catalog(family: str) -> list[dict]:
    response = get(f"{BASE_URL}/files/{family}", params={"current": "true"}, timeout=60)
    response.raise_for_status()
    rows = response.json()
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{family}: expected a non-empty file catalog")
    return rows


def _download_file(family: str, record: dict) -> bytes:
    url = (
        f"{BASE_URL}/files/{family}/{record['year']}/"
        f"{record['month']}/{record['version']}/download"
    )
    response = get(url, timeout=(30.0, 600.0))
    response.raise_for_status()
    return response.content


def _normalize_table(table: pa.Table, family: str, record: dict) -> pa.Table:
    source_cols = set(table.column_names)
    supported_cols = set(STRING_COLUMNS)
    unknown_cols = sorted(source_cols - supported_cols)
    if unknown_cols:
        raise ValueError(f"{record.get('filename')}: unexpected source columns: {unknown_cols}")

    row_count = table.num_rows
    arrays = []
    for col in STRING_COLUMNS:
        if col in source_cols:
            arrays.append(table[col].cast(pa.string()))
        else:
            arrays.append(pa.nulls(row_count, type=pa.string()))

    arrays.extend(
        [
            pa.array([family] * row_count, type=pa.string()),
            pa.array([record["filename"]] * row_count, type=pa.string()),
            pa.array([record.get("publishDate")] * row_count, type=pa.string()),
            pa.array([int(record["year"])] * row_count, type=pa.int16()),
            pa.array([int(record["month"])] * row_count, type=pa.int8()),
            pa.array([int(record["version"])] * row_count, type=pa.int16()),
        ]
    )
    return pa.Table.from_arrays(arrays, schema=SCHEMA)


def fetch_family(node_id: str) -> None:
    family = _family_from_node_id(node_id)
    records = _catalog(family)
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        fragment
        for fragment, metadata in list_raw_fragments(node_id, "parquet").items()
        if metadata.get("run_id") == run_id
    }

    for record in records:
        fragment = record["filename"]
        if fragment in done:
            continue
        content = _download_file(family, record)
        source_table = pq.read_table(io.BytesIO(content))
        normalized = _normalize_table(source_table, family, record)
        save_raw_parquet(normalized, node_id, fragment=fragment)


DOWNLOAD_SPECS = [
    NodeSpec(id="opm-accessions", fn=fetch_family),
    NodeSpec(id="opm-employment", fn=fetch_family),
    NodeSpec(id="opm-separations", fn=fetch_family),
]
