"""State Statistics Service of Ukraine SDMX downloads.

Each accepted entity is one SSSU SDMX dataflow. Dataflows have different DSDs,
so the raw download preserves the source SDMX-CSV response exactly and lets the
model stage profile each table's observed columns.
"""

from datetime import datetime
import csv
import io
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "state-statistics-service-of-ukraine"
SDMX_BASE = "https://stat.gov.ua/sdmx/workspaces/default:integration/registry/sdmx/2.1"
SDMX3_BASE = "https://stat.gov.ua/sdmx/workspaces/default:integration/registry/sdmx/3.0"

CSV_HEADERS = {
    "Accept": "text/csv",
    "Accept-Language": "en",
}

# Bounds on the key-slicing fallback: never split a dimension so wide that the
# splitting costs more requests than the slice, and stop descending eventually.
MAX_SPLIT_VALUES = 500
MAX_SPLIT_DEPTH = 4

_SPEC_TO_ENTITY = {
    f"{SLUG}-{entity_id.lower().replace('_', '-')}": entity_id
    for entity_id in ENTITY_IDS
}

_ENTITY_VERSION = {
    # Versions come from the accepted collect catalog. The v2.1 data endpoint
    # needs the comma-separated flowRef form: SSSU,{ID},{VERSION}.
    'DF_ACCOUNT_COSTS_ENV_PROTECTION': '7.0.0',
    'DF_ACCOUNT_OF_EMISSIONS_INTO_ATMOSPHERIC_AIR': '7.0.0',
    'DF_AGRICULTURAL_ACTIVITY_RURAL_AREAS': '13.0.0',
    'DF_AGRICULTURAL_PRODUCTS_AT_CONSTANT_PRICES': '16.0.0',
    'DF_AGR_MACHINERY_AVAILABILITY': '9.0.0',
    'DF_AIR_EMS_AGGR_PORTAL': '2.0.0',
    'DF_ANNUAL_NATIONAL_ACCOUNTS': '7.0.0',
    'DF_AREA_HARVESTS_CROP_YIELD_A': '2.0.0',
    'DF_AREA_HARVESTS_CROP_YIELD_M': '3.0.0',
    'DF_ARRIVAL_AGR_ANIMALS_PROCESSING_ENTERPRISE': '13.0.0',
    'DF_ARRIVAL_GRAPES_WINE_MATERIALS': '10.0.0',
    'DF_ASSETS_EQUITY_LIABILITIES_FINANCIAL_RESULTS_B_A': '3.0.0',
    'DF_ASSETS_EQUITY_LIABILITIES_FINANCIAL_RESULTS_B_Q': '3.0.0',
    'DF_ASSETS_EQUITY_LIABILITIES_FINANCIAL_RESULTS_FR_A': '8.0.0',
    'DF_ASSETS_EQUITY_LIABILITIES_FINANCIAL_RESULTS_FR_Q': '3.0.0',
    'DF_AVAILABILITY_OF_GRAIN_AT_ENTERPRISES': '8.0.0',
    'DF_AVAIL_MOVEMENT_NONCURR_ASSETS_DEPRECIATION': '12.0.0',
    'DF_AVIA_TRANSPORT_ENTRP_ACTIVITY_A': '3.0.0',
    'DF_AVIA_TRANSPORT_ENTRP_ACTIVITY_M': '3.0.0',
    'DF_BEGINING_COMPLETION_CONSTRUCTION': '26.0.0',
    'DF_BUSINESS_ACTIVITY_STATE_ENTERPRISE': '19.0.0',
    'DF_CAPITAL_INVESTMENTS_A': '3.0.1',
    'DF_CAPITAL_INVESTMENTS_Q': '4.0.0',
    'DF_COLLECTIVE_ACCOM_FACILITIES': '8.0.0',
    'DF_COMMUNAL_SERVICES': '14.0.0',
    'DF_CONSUMER_PRICES_FOR_NATURAL_GAS_AND_ELECTRICITY': '7.0.0',
    'DF_COSTS_OF_ENVIRONMENTAL_PROTECTION': '7.0.0',
    'DF_COST_AGR_PRODUCT': '16.0.0',
    'DF_DELIVERY_DAIRY_MATERIALS_PROC_MILK_PROD_A': '1.0.0',
    'DF_DELIVERY_DAIRY_MATERIALS_PROC_MILK_PROD_M': '3.0.0',
    'DF_DELIVERY_MILK_PROCESSING_ENTERPRISE': '11.0.0',
    'DF_DEMOGRAPHICS_OF_ENTERPRISES': '8.0.0',
    'DF_ECONOMIC_ACCOUNTS_AGRICULTURE': '8.0.0',
    'DF_ECONOMIC_ACTIVITY_OF_NON_FINANCIAL_SERVICES_ENTERPRISES': '6.0.0',
    'DF_ECONOMY_STRUCTURAL_CHANGES_BUSINESS_ENTITY': '10.0.1',
    'DF_ECONOMY_STRUCTURAL_CHANGES_ENTERPRISE': '11.0.0',
    'DF_ECONOM_INDC_SHORT-TERM_CONSTRUCTION_STAT': '16.0.0',
    'DF_EDUCATIONAL_INSTITUTIONS': '36.0.0',
    'DF_ENERGY_BALANCE': '4.0.0',
    'DF_ENTERPRISE_LABOR_STATISTICS': '23.0.0',
    'DF_EXPENSES_OF_ENTERPRISES_FOR_WORKFORCE_MAINTENANCE': '9.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS': '5.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS_BY_CLASSIFICATIONS': '3.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS_BY_PARTNER_COUNTRIES': '4.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS_BY_RAW_PRODUCT': '4.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS_M': '2.0.0',
    'DF_EXTERNAL_TRADE_OF_GOODS_M_Q': '4.0.0',
    'DF_FISHING_ACTIVITY': '9.0.0',
    'DF_FOREIGN_TRADE_SERVICES': '12.0.0',
    'DF_FOREIGN_TRADE_SERVICES_Q': '2.0.0',
    'DF_FORESTRY_ACTIVITY': '22.0.0',
    'DF_FUEL_USAGE_AND_RESERVES_A': '2.0.0',
    'DF_FUEL_USAGE_AND_RESERVES_M': '2.0.0',
    'DF_GROUND_TRANSPORT_A': '3.0.0',
    'DF_GROUND_TRANSPORT_M': '6.0.0',
    'DF_GROUND_TRANSPORT_Q': '3.0.0',
    'DF_HOUSEHOLD_ACCOUNT_OBJECT': '7.0.0',
    'DF_INDX_EXPENDITURE_AGR_PRODUCT': '2.0.0',
    'DF_IND_SHORT_STAT_INDUSTR_PROD': '20.0.0',
    'DF_IND_SHORT_STAT_INDUSTR_STAT': '14.0.0',
    'DF_INFORM_COMMUN_TECH_ENTRP': '9.0.0',
    'DF_INNOVATION_ENTERPRISE_ACTIVITY': '14.0.0',
    'DF_INTEGRATED_INDICATORS_OF_TRANSPORT_STATISTICS': '6.0.0',
    'DF_LABOR_FORCE_A': '2.0.1',
    'DF_LABOR_FORCE_Q': '2.0.1',
    'DF_MAIN_PRODUCTS_OF_AGRICULTURAL_PRODUCTION': '9.0.0',
    'DF_MANAGEMENT_OF_HUNTING': '7.0.0',
    'DF_PIPELINE_ENTRP_ACTIVITY': '14.0.0',
    'DF_POLLUTANTS_GASES_EMISSIONS': '16.0.0',
    'DF_POPULATION_BIRTH': '5.0.0',
    'DF_POPULATION_DEATH_CAUSE': '3.0.0',
    'DF_POPULATION_MARRIAGE_DIVORCE': '6.0.0',
    'DF_POPULATION_MIGRATION': '2.0.0',
    'DF_POPULATION_MORTALITY': '5.0.0',
    'DF_POPULATION_STRUCTURE': '8.0.0',
    'DF_PRICE_CHANGES_IMPORT': '1.0.0',
    'DF_PRICE_CHANGES_OF_SERVICE_PRODUCERS': '11.0.0',
    'DF_PRICE_CHANGE_CONSTRUCTION': '15.0.0',
    'DF_PRICE_CHANGE_CONSUMER_GOODS_SERVICE': '27.0.0',
    'DF_PRICE_CHANGE_HOUSING_MARKET': '16.0.0',
    'DF_PRICE_CHANGE_MANUFACTURER_INDUSTRIAL_PRODUCT': '21.0.0',
    'DF_PROD_SOLD_INDUSTRIAL_PRODUCTS_TYPE': '6.0.0',
    'DF_PURCHASE_MATERIAL_TECH_RESOURCE': '2.0.0',
    'DF_QUARTERLY_NATIONAL_ACCOUNTS': '14.0.0',
    'DF_REGIONAL_ACCOUNTS': '8.0.0',
    'DF_SALARY_LEVEL_OF_EMPLOYEES': '6.0.0',
    'DF_SALARY_PAYMENT_STATUS': '4.0.2',
    'DF_SALE_AGR_PROD_BY_ENTRPRS_HSHLD': '11.0.2',
    'DF_SALE_AND_STOCKS_OF_GOODS_RETAIL_A_Q': '5.0.0',
    'DF_SALE_AND_STOCKS_OF_GOODS_RETAIL_M': '4.0.0',
    'DF_SALE_AND_STOCKS_OF_GOODS_WHOLESALE_M': '3.0.0',
    'DF_SALE_AND_STOCKS_OF_GOODS_WHOLESALE_Q': '2.0.0',
    'DF_SATELLITE_ACCOUNT_OF_EDUCATION': '7.0.0',
    'DF_SATELLITE_HEALTHCARE_ACCOUNT': '6.0.0',
    'DF_SCIENTIFIC_RESEARCH_DEVELOPMENT': '30.0.1',
    'DF_SOCIAL_PROTECTION_SATELLITE_ACCOUNTS': '7.0.0',
    'DF_STATISTICAL_BUSINESS_REGISTER_A': '2.0.0',
    'DF_STATISTICAL_BUSINESS_REGISTER_Q_M': '2.0.1',
    'DF_STATISTICAL_INDICATORS_DEMOGRAPHY_ENTERPRISES': '6.0.0',
    'DF_STOCKBREEDING_FODDER_A': '5.0.2',
    'DF_STOCKBREEDING_FODDER_M': '6.0.0',
    'DF_SUPPLY_USE_ENERGY': '15.0.0',
    'DF_SURVEY_LIVING_CONDITIONS_HOUSEHOLDS_A': '2.0.0',
    'DF_SURVEY_LIVING_CONDITIONS_HOUSEHOLDS_Q': '3.0.0',
    'DF_USE_FERTILIZERS_PESTICIDES_HARVEST_AGR_CROPS': '12.0.0',
    'DF_WASTE_GENERATION_MANAGEMENT_AGGREGATED_INDICATORS': '13.0.0',
    'DF_WASTE_GENERATION_MANAGEMENT_TREATMENT_FACILITIES': '5.0.0',
    'DF_WATER_TRANSPORT_ENTRP_ACTIVITY_A': '3.0.0',
    'DF_WATER_TRANSPORT_ENTRP_ACTIVITY_M': '6.0.0',
    'DF_WATER_TRANSPORT_ENTRP_ACTIVITY_Q': '3.0.0',
    'DF_WORKING_CONDITIONS_ENTERPRISES': '7.0.0',
    'DF_WORKPLACE_TRAUMATISM': '7.0.0',
}


def _looks_like_sdmx_csv(content: bytes) -> bool:
    head = content[:4096].decode("utf-8-sig", "replace")
    return "DATAFLOW" in head and "TIME_PERIOD" in head and "OBS_VALUE" in head and "\n" in head


def _normalized_sdmx_csv(content: bytes) -> bytes:
    text = content.decode("utf-8-sig", "replace")
    reader = csv.reader(io.StringIO(text))
    rows = []
    columns = None
    for row in reader:
        row = [" ".join(cell.split()) for cell in row]
        if not row or not any(cell.strip() for cell in row):
            continue
        if columns is None:
            columns = row
            rows.append(row)
            continue
        if len(row) == len(columns):
            rows.append(row)

    if columns is None:
        return b""

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def _csv_row_count(content: bytes) -> int:
    normalized = _normalized_sdmx_csv(content)
    if not normalized:
        return 0
    text = normalized.decode("utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    return max(len(lines) - 1, 0)


def _csv_to_table(content: bytes) -> pa.Table:
    normalized = _normalized_sdmx_csv(content)
    if not normalized:
        raise ValueError("SDMX-CSV response had no header")
    header = normalized.splitlines()[0].decode("utf-8")
    columns = next(csv.reader(io.StringIO(header)))
    return pacsv.read_csv(
        pa.BufferReader(normalized),
        read_options=pacsv.ReadOptions(encoding="utf8"),
        convert_options=pacsv.ConvertOptions(
            column_types={column: pa.string() for column in columns},
            strings_can_be_null=True,
        ),
    )


def _save_sdmx_csv(content: bytes, node_id: str, *, fragment: str | None = None) -> None:
    save_raw_parquet(_csv_to_table(content), node_id, fragment=fragment)


def _year(value: str) -> int:
    match = re.search(r"\d{4}", value or "")
    if not match:
        raise ValueError(f"cannot read year from availability value {value!r}")
    return int(match.group(0))


def _availability(entity_id: str, version: str, key: str | None = None) -> dict:
    path = f"{entity_id}/{version}" if key is None else f"{entity_id}/{version}/{key}"
    url = f"{SDMX3_BASE}/availability/dataflow/SSSU/{path}/all"
    response = get(url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    response.raise_for_status()
    payload = response.json()
    constraints = payload.get("data", {}).get("dataConstraints", [])
    if not constraints:
        raise ValueError(f"{entity_id}: availability response has no data constraints")
    return constraints[0]


def _availability_years(entity_id: str, version: str) -> range:
    annotations = _availability(entity_id, version).get("annotations", [])
    metrics = {
        item.get("id"): item.get("title")
        for item in annotations
        if item.get("type") == "sdmx_metrics"
    }
    start = _year(metrics.get("time_period_start", ""))
    end = min(_year(metrics.get("time_period_end", "")), datetime.utcnow().year)
    if end < start:
        raise ValueError(f"{entity_id}: invalid availability range {start}..{end}")
    return range(start, end + 1)


def _availability_values(
    entity_id: str, version: str, key: str | None = None
) -> dict[str, list[str]]:
    """Per-slice allowed values, keyed by dimension id."""
    regions = _availability(entity_id, version, key).get("cubeRegions", [])
    if not regions:
        return {}
    return {
        component["id"]: [value["value"] for value in component.get("values", [])]
        for component in regions[0].get("components", [])
    }


def _dimension_order(entity_id: str, version: str) -> list[str]:
    """Key dimension ids in DSD position order (the dotted key's slot order)."""
    url = f"{SDMX_BASE}/dataflow/SSSU/{entity_id}/{version}"
    response = get(url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    response.raise_for_status()
    dataflows = response.json().get("data", {}).get("dataflows", [])
    if not dataflows:
        raise ValueError(f"{entity_id}: dataflow {version} not found upstream")

    match = re.search(r"DataStructure=([^:]+):([^(]+)\(([^)]+)\)", dataflows[0]["structure"])
    if not match:
        raise ValueError(f"{entity_id}: cannot read DSD from {dataflows[0]['structure']!r}")
    agency, dsd_id, dsd_version = match.groups()

    dsd_url = f"{SDMX_BASE}/datastructure/{agency}/{dsd_id}/{dsd_version}?references=none"
    dsd_response = get(dsd_url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    dsd_response.raise_for_status()
    structures = dsd_response.json().get("data", {}).get("dataStructures", [])
    if not structures:
        raise ValueError(f"{entity_id}: DSD {dsd_id} {dsd_version} not found upstream")
    dimensions = structures[0]["dataStructureComponents"]["dimensionList"]["dimensions"]
    return [item["id"] for item in sorted(dimensions, key=lambda item: item["position"])]


def _fetch_csv(url: str) -> bytes | None:
    response = get(url, headers=CSV_HEADERS, timeout=(10.0, 900.0))
    if response.status_code >= 400:
        return None
    content = response.content
    if not _looks_like_sdmx_csv(content):
        return None
    return content


def _fragment_name(dimensions: list[str], key_parts: list[str]) -> str:
    return "__".join(
        f"{dimension.lower()}-{re.sub(r'[^0-9A-Za-z_]+', '-', value)}"
        for dimension, value in zip(dimensions, key_parts)
        if value
    )


def _fetch_key_slices(
    entity_id: str,
    version: str,
    node_id: str,
    dimensions: list[str],
    key_parts: list[str],
    depth: int,
) -> int:
    """Fetch one key slice, splitting on a dimension when the server can't build it.

    SSSU answers 500 for slices that are too large to render, and the size is
    driven by the series count rather than the time range — so a slice that the
    yearly requests can't shrink is split along its own availability instead.

    An all-empty key goes straight to the split: that request is the unsliced one
    `fetch_one` has already tried.
    """
    # Both endpoints want the key omitted entirely rather than left all-empty.
    key = ".".join(key_parts) if any(key_parts) else None
    if key is not None:
        content = _fetch_csv(f"{SDMX_BASE}/data/SSSU,{entity_id},{version}/{key}")
        if content is not None:
            if _csv_row_count(content) == 0:
                return 0
            _save_sdmx_csv(content, node_id, fragment=_fragment_name(dimensions, key_parts))
            return 1

    if depth >= MAX_SPLIT_DEPTH:
        return 0

    available = _availability_values(entity_id, version, key)
    for index, dimension in enumerate(dimensions):
        if key_parts[index]:
            continue
        values = available.get(dimension, [])
        # A single-valued dimension doesn't shrink the slice; a huge one (goods
        # codes) would cost more requests than the split can repay.
        if not 1 < len(values) <= MAX_SPLIT_VALUES:
            continue
        saved = 0
        for value in values:
            child = list(key_parts)
            child[index] = value
            saved += _fetch_key_slices(
                entity_id, version, node_id, dimensions, child, depth + 1
            )
        return saved

    return 0


def fetch_one(node_id: str) -> None:
    entity_id = _SPEC_TO_ENTITY[node_id]
    version = _ENTITY_VERSION[entity_id]
    url = f"{SDMX_BASE}/data/SSSU,{entity_id},{version}"
    content = _fetch_csv(url)
    if content is not None:
        _save_sdmx_csv(content, node_id)
        return

    saved = 0
    for year in _availability_years(entity_id, version):
        part_url = f"{url}?startPeriod={year}&endPeriod={year}"
        part = _fetch_csv(part_url)
        if part is None or _csv_row_count(part) == 0:
            continue
        _save_sdmx_csv(part, node_id, fragment=str(year))
        saved += 1
    if saved:
        return

    dimensions = _dimension_order(entity_id, version)
    saved = _fetch_key_slices(
        entity_id, version, node_id, dimensions, [""] * len(dimensions), 0
    )
    if saved == 0:
        raise ValueError(
            f"{entity_id}: no SDMX-CSV rows returned by full, yearly or key-sliced requests"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
