"""INFORM (JRC) downloads from the public INFORM REST API."""

from __future__ import annotations

import re
from typing import Any

import pyarrow as pa

from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, raw_parquet_writer, save_raw_parquet


BASE_URL = "https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/"
TIMEOUT = (10.0, 300.0)


COUNTRIES_SCHEMA = pa.schema(
    [
        ("continent", pa.string()),
        ("category_type", pa.string()),
        ("admin_level", pa.string()),
        ("category_info", pa.string()),
        ("income_value", pa.string()),
        ("notes", pa.string()),
        ("iso3", pa.string()),
        ("country_name", pa.string()),
        ("iso_group", pa.string()),
    ]
)

INDICATORS_SCHEMA = pa.schema(
    [
        ("indicator_id", pa.string()),
        ("indicator_type", pa.string()),
        ("indicator_description", pa.string()),
        ("indicator_note", pa.string()),
        ("provider", pa.string()),
        ("default_weight", pa.float64()),
        ("missing_value", pa.float64()),
        ("unit", pa.string()),
        ("indicator_group", pa.string()),
        ("note", pa.string()),
        ("link", pa.string()),
    ]
)

WORKFLOWS_SCHEMA = pa.schema(
    [
        ("workflow_id", pa.int64()),
        ("name", pa.string()),
        ("workflow_group_name", pa.string()),
        ("system", pa.string()),
        ("gna_year", pa.int32()),
        ("workflow_date", pa.string()),
        ("gna_from_date", pa.string()),
        ("gna_to_date", pa.string()),
        ("flag_methodology_approved", pa.string()),
        ("flag_data_saved", pa.string()),
        ("flag_gna_published", pa.string()),
        ("author", pa.string()),
        ("comments", pa.string()),
        ("workflow_compare_id", pa.int64()),
        ("version", pa.string()),
        ("geometry_filename", pa.string()),
        ("use_prediction", pa.bool_()),
        ("methodology_id", pa.int64()),
        ("methodology_description", pa.string()),
        ("category_info", pa.string()),
        ("model_type", pa.string()),
        ("iso3", pa.string()),
        ("new_workflow_group_name", pa.string()),
        ("new_system_name", pa.string()),
        ("is_reference", pa.bool_()),
        ("score_family", pa.string()),
    ]
)

SCORES_SCHEMA = pa.schema(
    [
        ("workflow_id", pa.int64()),
        ("workflow_name", pa.string()),
        ("workflow_group_name", pa.string()),
        ("gna_year", pa.int32()),
        ("score_family", pa.string()),
        ("geo_id", pa.string()),
        ("indicator_id", pa.string()),
        ("indicator_name", pa.string()),
        ("indicator_score", pa.float64()),
        ("node_level", pa.int32()),
        ("validity_year", pa.int32()),
        ("unit", pa.string()),
        ("note", pa.string()),
    ]
)


def _json(path: str, params: dict[str, Any] | None = None) -> Any:
    resp = get(BASE_URL + path, params=params, headers={"Accept": "application/json"}, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _is_global_group(group: str | None) -> bool:
    return bool(group and re.match(r"^INFORM20[0-9]{2}", group))


def _score_family(group: str | None) -> str:
    return "global" if _is_global_group(group) else "subnational"


def _workflow_groups() -> list[str]:
    groups = _json("Workflows/WorkflowGroups")
    if not isinstance(groups, list) or not groups:
        raise AssertionError("Workflows/WorkflowGroups returned no groups")
    return [str(group) for group in groups]


def _workflows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in _workflow_groups():
        group_rows = _json(f"Workflows/GetByWorkflowGroup/{group}")
        if not isinstance(group_rows, list):
            raise AssertionError(f"{group}: expected workflow list, got {type(group_rows).__name__}")
        for row in group_rows:
            row = dict(row)
            row["score_family"] = _score_family(row.get("WorkflowGroupName") or group)
            rows.append(row)
    if not rows:
        raise AssertionError("no workflows discovered")
    return rows


def _countries_table(rows: list[dict[str, Any]]) -> pa.Table:
    return pa.table(
        {
            "continent": [_str(r.get("Continent")) for r in rows],
            "category_type": [_str(r.get("CategoryType")) for r in rows],
            "admin_level": [_str(r.get("AdminLevel")) for r in rows],
            "category_info": [_str(r.get("CategoryInfo")) for r in rows],
            "income_value": [_str(r.get("IncomeValue")) for r in rows],
            "notes": [_str(r.get("Notes")) for r in rows],
            "iso3": [_str(r.get("Iso3")) for r in rows],
            "country_name": [_str(r.get("CountryName")) for r in rows],
            "iso_group": [_str(r.get("IsoGroup")) for r in rows],
        },
        schema=COUNTRIES_SCHEMA,
    )


def _indicators_table(rows: list[dict[str, Any]]) -> pa.Table:
    return pa.table(
        {
            "indicator_id": [_str(r.get("IndicatorId")) for r in rows],
            "indicator_type": [_str(r.get("IndicatorType")) for r in rows],
            "indicator_description": [_str(r.get("IndicatorDescription")) for r in rows],
            "indicator_note": [_str(r.get("IndicatorNote")) for r in rows],
            "provider": [_str(r.get("Provider")) for r in rows],
            "default_weight": [_float(r.get("DefaultWeight")) for r in rows],
            "missing_value": [_float(r.get("MissingValue")) for r in rows],
            "unit": [_str(r.get("Unit")) for r in rows],
            "indicator_group": [_str(r.get("IndicatorGroup")) for r in rows],
            "note": [_str(r.get("Note")) for r in rows],
            "link": [_str(r.get("Link")) for r in rows],
        },
        schema=INDICATORS_SCHEMA,
    )


def _workflows_table(rows: list[dict[str, Any]]) -> pa.Table:
    return pa.table(
        {
            "workflow_id": [_int(r.get("WorkflowId")) for r in rows],
            "name": [_str(r.get("Name")) for r in rows],
            "workflow_group_name": [_str(r.get("WorkflowGroupName")) for r in rows],
            "system": [_str(r.get("System")) for r in rows],
            "gna_year": [_int(r.get("GNAYear")) for r in rows],
            "workflow_date": [_str(r.get("WorkflowDate")) for r in rows],
            "gna_from_date": [_str(r.get("GNAFromDate")) for r in rows],
            "gna_to_date": [_str(r.get("GNAToDate")) for r in rows],
            "flag_methodology_approved": [_str(r.get("FlagMethodologyApproved")) for r in rows],
            "flag_data_saved": [_str(r.get("FlagDataSaved")) for r in rows],
            "flag_gna_published": [_str(r.get("FlagGnaPublished")) for r in rows],
            "author": [_str(r.get("Author")) for r in rows],
            "comments": [_str(r.get("Comments")) for r in rows],
            "workflow_compare_id": [_int(r.get("WorkflowCompareId")) for r in rows],
            "version": [_str(r.get("Version")) for r in rows],
            "geometry_filename": [_str(r.get("GeometryFilename")) for r in rows],
            "use_prediction": [r.get("UsePrediction") for r in rows],
            "methodology_id": [_int(r.get("MethodologyId")) for r in rows],
            "methodology_description": [_str(r.get("MethodologyDescription")) for r in rows],
            "category_info": [_str(r.get("CategoryInfo")) for r in rows],
            "model_type": [_str(r.get("ModelType")) for r in rows],
            "iso3": [_str(r.get("Iso3")) for r in rows],
            "new_workflow_group_name": [_str(r.get("NewWorkflowGroupName")) for r in rows],
            "new_system_name": [_str(r.get("NewSystemName")) for r in rows],
            "is_reference": [r.get("IsReference") for r in rows],
            "score_family": [_str(r.get("score_family")) for r in rows],
        },
        schema=WORKFLOWS_SCHEMA,
    )


def _scores_table(workflow: dict[str, Any], rows: list[dict[str, Any]]) -> pa.Table:
    workflow_id = _int(workflow.get("WorkflowId"))
    group = _str(workflow.get("WorkflowGroupName"))
    return pa.table(
        {
            "workflow_id": [workflow_id for _ in rows],
            "workflow_name": [_str(workflow.get("Name")) for _ in rows],
            "workflow_group_name": [group for _ in rows],
            "gna_year": [_int(workflow.get("GNAYear")) for _ in rows],
            "score_family": [_score_family(group) for _ in rows],
            "geo_id": [_str(r.get("Iso3")) for r in rows],
            "indicator_id": [_str(r.get("IndicatorId")) for r in rows],
            "indicator_name": [_str(r.get("IndicatorName")) for r in rows],
            "indicator_score": [_float(r.get("IndicatorScore")) for r in rows],
            "node_level": [_int(r.get("nodelevel")) for r in rows],
            "validity_year": [_int(r.get("ValidityYear")) for r in rows],
            "unit": [_str(r.get("Unit")) for r in rows],
            "note": [_str(r.get("Note")) for r in rows],
        },
        schema=SCORES_SCHEMA,
    )


def fetch_countries(node_id: str) -> None:
    rows = _json("Countries/Index/")
    if not isinstance(rows, list) or len(rows) < 200:
        raise AssertionError(f"{node_id}: expected country/admin list, got {len(rows) if isinstance(rows, list) else 0}")
    save_raw_parquet(_countries_table(rows), node_id)


def fetch_indicators(node_id: str) -> None:
    rows = _json("Indicators/Index/")
    if not isinstance(rows, list) or len(rows) < 300:
        raise AssertionError(f"{node_id}: expected hundreds of indicators, got {len(rows) if isinstance(rows, list) else 0}")
    save_raw_parquet(_indicators_table(rows), node_id)


def fetch_workflows(node_id: str) -> None:
    rows = _workflows()
    save_raw_parquet(_workflows_table(rows), node_id)


def _fetch_scores(node_id: str, family: str) -> None:
    workflows = [row for row in _workflows() if row.get("score_family") == family]
    if not workflows:
        raise AssertionError(f"{node_id}: discovered no {family} workflows")
    written = 0
    with raw_parquet_writer(node_id, SCORES_SCHEMA) as writer:
        for workflow in workflows:
            workflow_id = _int(workflow.get("WorkflowId"))
            rows = _json("Countries/Scores/", params={"WorkflowId": workflow_id})
            if not isinstance(rows, list):
                raise AssertionError(f"{node_id}: workflow {workflow_id} did not return a list")
            if not rows:
                continue
            writer.write_table(_scores_table(workflow, rows))
            written += len(rows)
    if written == 0:
        raise AssertionError(f"{node_id}: wrote zero score rows")


def fetch_global_scores(node_id: str) -> None:
    _fetch_scores(node_id, "global")


def fetch_subnational_scores(node_id: str) -> None:
    _fetch_scores(node_id, "subnational")


DOWNLOAD_SPECS = [
    NodeSpec(id="inform-countries", fn=fetch_countries),
    NodeSpec(id="inform-indicators", fn=fetch_indicators),
    NodeSpec(id="inform-inform-risk-scores", fn=fetch_global_scores),
    NodeSpec(id="inform-inform-subnational-scores", fn=fetch_subnational_scores),
    NodeSpec(id="inform-workflows", fn=fetch_workflows),
]

_CADENCE = "Refetch at least monthly; INFORM Risk publishes roughly twice yearly per https://drmkc.jrc.ec.europa.eu/inform-index."

MAINTAIN_SPECS = [
    MaintainSpec(asset_id=spec.id, description=_CADENCE, check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=30))
    for spec in DOWNLOAD_SPECS
]
