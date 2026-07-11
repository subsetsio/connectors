from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


BASE_URL = "https://gsu-prod.ipc.codes/api/ptt"
CLASSIFICATIONS = ("AFI", "CFI")
START_YEAR = 2000
END_YEAR = 2030
SPEC_PREFIX = "ipc-food-security-"


COUNTRIES_SCHEMA = pa.schema(
    [
        pa.field("country_code", pa.string()),
        pa.field("country_name", pa.string()),
        pa.field("region", pa.string()),
        pa.field("has_data", pa.bool_()),
    ]
)

ANALYSES_SCHEMA = pa.schema(
    [
        pa.field("anl_id", pa.string()),
        pa.field("country_code", pa.string()),
        pa.field("classification", pa.string()),
        pa.field("title", pa.string()),
        pa.field("analysis_date", pa.timestamp("us", tz="UTC")),
        pa.field("fanalysis_date", pa.timestamp("us", tz="UTC")),
        pa.field("country_population", pa.int64()),
        pa.field("public_map_link", pa.string()),
        pa.field("public_map_title", pa.string()),
        pa.field("has_groups", pa.bool_()),
        pa.field("period_count", pa.int64()),
    ]
)

NATIONAL_SCHEMA = pa.schema(
    [
        pa.field("anl_id", pa.string()),
        pa.field("country_code", pa.string()),
        pa.field("classification", pa.string()),
        pa.field("period_code", pa.string()),
        pa.field("period_name", pa.string()),
        pa.field("period_type", pa.string()),
        pa.field("period_from_date", pa.timestamp("us", tz="UTC")),
        pa.field("period_thru_date", pa.timestamp("us", tz="UTC")),
        pa.field("analysis_date", pa.timestamp("us", tz="UTC")),
        pa.field("analyzed_population", pa.int64()),
        pa.field("phase1_population", pa.int64()),
        pa.field("phase1_percentage", pa.float64()),
        pa.field("phase2_population", pa.int64()),
        pa.field("phase2_percentage", pa.float64()),
        pa.field("phase3_population", pa.int64()),
        pa.field("phase3_percentage", pa.float64()),
        pa.field("phase4_population", pa.int64()),
        pa.field("phase4_percentage", pa.float64()),
        pa.field("phase5_population", pa.int64()),
        pa.field("phase5_percentage", pa.float64()),
        pa.field("phase3_plus_population", pa.int64()),
        pa.field("phase3_plus_percentage", pa.float64()),
    ]
)

AREA_SCHEMA = pa.schema(
    [
        pa.field("anl_id", pa.string()),
        pa.field("country_code", pa.string()),
        pa.field("analysis_classification", pa.string()),
        pa.field("analysis_date", pa.timestamp("us", tz="UTC")),
        pa.field("group_id", pa.string()),
        pa.field("group_name", pa.string()),
        pa.field("aar_id", pa.string()),
        pa.field("area", pa.string()),
        pa.field("period_code", pa.string()),
        pa.field("period_title", pa.string()),
        pa.field("period_from_date", pa.timestamp("us", tz="UTC")),
        pa.field("period_thru_date", pa.timestamp("us", tz="UTC")),
        pa.field("estimated_population", pa.int64()),
        pa.field("census_population", pa.int64()),
        pa.field("overall_phase_value", pa.int64()),
        pa.field("overall_phase_label", pa.string()),
        pa.field("overall_trend", pa.string()),
        pa.field("classification_text", pa.string()),
        pa.field("hfa_population_percentage", pa.float64()),
        pa.field("hfa_kcal_percentage", pa.float64()),
        pa.field("hfa_significance_value", pa.int64()),
        pa.field("hfa_significance_label", pa.string()),
        pa.field("phase1_population", pa.int64()),
        pa.field("phase1_percentage", pa.float64()),
        pa.field("phase2_population", pa.int64()),
        pa.field("phase2_percentage", pa.float64()),
        pa.field("phase3_population", pa.int64()),
        pa.field("phase3_percentage", pa.float64()),
        pa.field("phase4_population", pa.int64()),
        pa.field("phase4_percentage", pa.float64()),
        pa.field("phase5_population", pa.int64()),
        pa.field("phase5_percentage", pa.float64()),
        pa.field("phase3_plus_population", pa.int64()),
        pa.field("phase3_plus_percentage", pa.float64()),
    ]
)


def _json(path: str, params: dict[str, Any] | None = None) -> Any:
    response = get(f"{BASE_URL}{path}", params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text).astimezone(timezone.utc)


def _to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _countries() -> list[dict[str, Any]]:
    regions = _json("/regions")
    rows = []
    for region, countries in sorted(regions.items()):
        for country in countries:
            rows.append(
                {
                    "country_code": country.get("code"),
                    "country_name": country.get("name"),
                    "region": region,
                    "has_data": bool(country.get("hasData")),
                }
            )
    return rows


def _country_codes_with_data() -> list[str]:
    return [row["country_code"] for row in _countries() if row["has_data"]]


def _analyses() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for country_code in _country_codes_with_data():
        for classification in CLASSIFICATIONS:
            payload = _json(
                f"/data-with-meta/{START_YEAR},{END_YEAR}",
                params={"classification": classification, "country": country_code},
            )
            rows.extend(payload.get("data") or [])
    return rows


def _period_lookup(analysis: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        period.get("period_code"): period
        for period in (analysis.get("periods") or [])
        if period.get("period_code")
    }


def _analysis_row(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "anl_id": str(analysis.get("anl_id")),
        "country_code": analysis.get("country"),
        "classification": analysis.get("classification"),
        "title": analysis.get("title"),
        "analysis_date": _parse_ts(analysis.get("analysis_date")),
        "fanalysis_date": _parse_ts(analysis.get("fanalysis_date")),
        "country_population": _to_int(analysis.get("country_population")),
        "public_map_link": analysis.get("public_map_link"),
        "public_map_title": analysis.get("public_map_title"),
        "has_groups": bool(analysis.get("has_groups")),
        "period_count": len(analysis.get("periods") or []),
    }


def _national_rows() -> list[dict[str, Any]]:
    rows = []
    for analysis in _analyses():
        periods = _period_lookup(analysis)
        for period_code, totals in (analysis.get("totals") or {}).items():
            period = periods.get(period_code) or {}
            rows.append(
                {
                    "anl_id": str(analysis.get("anl_id")),
                    "country_code": analysis.get("country"),
                    "classification": analysis.get("classification"),
                    "period_code": period_code,
                    "period_name": period.get("name"),
                    "period_type": period.get("period_type"),
                    "period_from_date": _parse_ts(period.get("from_date")),
                    "period_thru_date": _parse_ts(period.get("thru_date")),
                    "analysis_date": _parse_ts(analysis.get("analysis_date")),
                    "analyzed_population": _to_int(totals.get("analyzedPopulation")),
                    "phase1_population": _to_int(totals.get("phase1Population")),
                    "phase1_percentage": _to_float(totals.get("phase1Percentage")),
                    "phase2_population": _to_int(totals.get("phase2Population")),
                    "phase2_percentage": _to_float(totals.get("phase2Percentage")),
                    "phase3_population": _to_int(totals.get("phase3Population")),
                    "phase3_percentage": _to_float(totals.get("phase3Percentage")),
                    "phase4_population": _to_int(totals.get("phase4Population")),
                    "phase4_percentage": _to_float(totals.get("phase4Percentage")),
                    "phase5_population": _to_int(totals.get("phase5Population")),
                    "phase5_percentage": _to_float(totals.get("phase5Percentage")),
                    "phase3_plus_population": _to_int(totals.get("phase3PlusPopulation")),
                    "phase3_plus_percentage": _to_float(totals.get("phase3PlusPercentage")),
                }
            )
    return rows


def _area_source_records(analysis: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    if analysis.get("has_groups"):
        records = []
        for group in analysis.get("groups") or []:
            for area in group.get("areas") or []:
                records.append((area, group))
        return records
    return [(area, None) for area in analysis.get("areas") or []]


def _area_rows() -> list[dict[str, Any]]:
    rows = []
    for analysis in _analyses():
        for area, group in _area_source_records(analysis):
            for period_code, period in (area.get("periods") or {}).items():
                rows.append(
                    {
                        "anl_id": str(analysis.get("anl_id")),
                        "country_code": analysis.get("country"),
                        "analysis_classification": analysis.get("classification"),
                        "analysis_date": _parse_ts(analysis.get("analysis_date")),
                        "group_id": None if group is None else str(group.get("group_id")),
                        "group_name": None if group is None else group.get("group_name"),
                        "aar_id": str(period.get("aar_id") or area.get("aar_id")),
                        "area": period.get("area") or area.get("area"),
                        "period_code": period.get("period") or period_code,
                        "period_title": period.get("period_title"),
                        "period_from_date": _parse_ts(period.get("from_date")),
                        "period_thru_date": _parse_ts(period.get("thru_date")),
                        "estimated_population": _to_int(period.get("estimated_population")),
                        "census_population": _to_int(period.get("census_population")),
                        "overall_phase_value": _to_int(period.get("overall_phase_value")),
                        "overall_phase_label": period.get("overall_phase_label"),
                        "overall_trend": period.get("overall_trend"),
                        "classification_text": period.get("classification"),
                        "hfa_population_percentage": _to_float(period.get("hfa_population_percentage")),
                        "hfa_kcal_percentage": _to_float(period.get("hfa_kcal_percentage")),
                        "hfa_significance_value": _to_int(period.get("hfa_significance_value")),
                        "hfa_significance_label": period.get("hfa_significance_label"),
                        "phase1_population": _to_int(period.get("phase1_population")),
                        "phase1_percentage": _to_float(period.get("phase1_percentage")),
                        "phase2_population": _to_int(period.get("phase2_population")),
                        "phase2_percentage": _to_float(period.get("phase2_percentage")),
                        "phase3_population": _to_int(period.get("phase3_population")),
                        "phase3_percentage": _to_float(period.get("phase3_percentage")),
                        "phase4_population": _to_int(period.get("phase4_population")),
                        "phase4_percentage": _to_float(period.get("phase4_percentage")),
                        "phase5_population": _to_int(period.get("phase5_population")),
                        "phase5_percentage": _to_float(period.get("phase5_percentage")),
                        "phase3_plus_population": _to_int(period.get("phase3_plus_population")),
                        "phase3_plus_percentage": _to_float(period.get("phase3_plus_percentage")),
                    }
                )
    return rows


def _save(rows: list[dict[str, Any]], schema: pa.Schema, node_id: str) -> None:
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), node_id)


def fetch_one(node_id: str) -> None:
    entity_id = node_id.removeprefix(SPEC_PREFIX).replace("-", "_")
    if entity_id == "countries":
        _save(_countries(), COUNTRIES_SCHEMA, node_id)
    elif entity_id == "analyses":
        _save([_analysis_row(row) for row in _analyses()], ANALYSES_SCHEMA, node_id)
    elif entity_id == "national_estimates":
        _save(_national_rows(), NATIONAL_SCHEMA, node_id)
    elif entity_id == "area_estimates":
        _save(_area_rows(), AREA_SCHEMA, node_id)
    else:
        raise ValueError(f"unknown entity id for {node_id}")


DOWNLOAD_SPECS = [
    NodeSpec(id="ipc-food-security-analyses", fn=fetch_one),
    NodeSpec(id="ipc-food-security-area-estimates", fn=fetch_one),
    NodeSpec(id="ipc-food-security-countries", fn=fetch_one),
    NodeSpec(id="ipc-food-security-national-estimates", fn=fetch_one),
]
