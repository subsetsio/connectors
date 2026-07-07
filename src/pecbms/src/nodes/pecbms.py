from __future__ import annotations

import re
from typing import Any

import pyarrow as pa
from lxml import html
from subsets_utils import NodeSpec, get, post, save_raw_parquet


BASE_URL = "https://pecbms.info"
SPECIES_URL = f"{BASE_URL}/trends-and-indicators/species-trends/"
INDICATORS_URL = f"{BASE_URL}/trends-and-indicators/indicators/"
HOME_URL = f"{BASE_URL}/"
AJAX_URL = f"{BASE_URL}/wp-admin/admin-ajax.php"


def _text(node: Any) -> str:
    return re.sub(r"\s+", " ", node.text_content()).strip()


def _page(url: str) -> str:
    response = get(url, timeout=(10.0, 90.0))
    response.raise_for_status()
    return response.text


def _nonce(page_text: str) -> str:
    match = re.search(r'"wpj_nonce":"([^"]+)"', page_text)
    if not match:
        raise RuntimeError("Could not find wpj_nonce in page HTML")
    return match.group(1)


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip().replace(",", "")
    if not value or value in {"-", "NA", "N/A"}:
        return None
    return int(value)


def _float_or_none(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip().replace(",", "")
    if not value or value in {"-", "NA", "N/A"}:
        return None
    return float(value)


def _parse_slope(value: str) -> tuple[float | None, float | None]:
    match = re.match(r"([0-9.]+)\s*(?:\(([0-9.]+)\))?", value)
    if not match:
        return None, None
    return _float_or_none(match.group(1)), _float_or_none(match.group(2))


def _species_rows(page_text: str) -> list[dict[str, Any]]:
    root = html.fromstring(page_text)
    rows: list[dict[str, Any]] = []
    for tr in root.xpath('//table[@id="bird__table"]//tbody/tr'):
        cells = tr.xpath("./td")
        if len(cells) < 6:
            continue
        input_nodes = cells[0].xpath('.//input[@name="species[]"]')
        if not input_nodes:
            continue
        species_id = input_nodes[0].get("value")
        species_name = _text(cells[0])
        long_slope, long_slope_se = _parse_slope(_text(cells[2]))
        ten_year_slope, ten_year_slope_se = _parse_slope(_text(cells[4]))
        rows.append(
            {
                "species_id": species_id,
                "species_name": species_name,
                "long_term_trend_percent": _int_or_none(_text(cells[1])),
                "long_term_slope": long_slope,
                "long_term_slope_se": long_slope_se,
                "ten_year_trend_percent": _int_or_none(_text(cells[3])),
                "ten_year_slope": ten_year_slope,
                "ten_year_slope_se": ten_year_slope_se,
                "habitat": _text(cells[5]).lower() or None,
            }
        )
    return rows


def _indicator_rows(page_text: str) -> list[dict[str, Any]]:
    root = html.fromstring(page_text)
    rows: list[dict[str, Any]] = []
    current_group = None
    container = root.xpath('//div[@id="indicator__table"]')
    if not container:
        raise RuntimeError("Could not find indicator__table")
    for node in container[0].iterchildren():
        if node.tag == "h2":
            current_group = _text(node)
            continue
        for tr in node.xpath('.//table[contains(@class, "indicator__table")]//tbody/tr'):
            cells = tr.xpath("./td")
            if len(cells) < 5:
                continue
            input_nodes = cells[0].xpath('.//input[@name="indicataors[]"]')
            if not input_nodes:
                continue
            rows.append(
                {
                    "indicator_id": input_nodes[0].get("value"),
                    "indicator_name": _text(cells[0]),
                    "indicator_group": current_group,
                    "region": _text(cells[1]),
                    "time_period": _text(cells[2]),
                    "species_count": _int_or_none(_text(cells[3])),
                    "trend_percent": _int_or_none(_text(cells[4])),
                }
            )
    return rows


def _chart_rows(
    page_text: str,
    chart_ids: list[str],
    action: str,
    id_col: str,
) -> list[dict[str, Any]]:
    nonce = _nonce(page_text)
    data: list[tuple[str, str]] = [
        ("security", nonce),
        ("action", action),
        ("all", "0"),
        ("conf", "0"),
    ]
    data.extend(("charts[]", chart_id) for chart_id in chart_ids)
    response = post(AJAX_URL, data=data, timeout=(10.0, 120.0))
    response.raise_for_status()
    charts = response.text
    pattern = re.compile(
        r"new Chart\(document\.getElementById\('([^']+)'\).*?"
        r"labels:\s*\[([^\]]*)\].*?"
        r"data:\s*\[([^\]]*)\]",
        re.S,
    )
    rows: list[dict[str, Any]] = []
    seen = set()
    for chart_id, labels_raw, values_raw in pattern.findall(charts):
        years = [_int_or_none(part) for part in labels_raw.split(",")]
        values = [_float_or_none(part) for part in values_raw.split(",")]
        if len(years) != len(values):
            raise RuntimeError(f"{chart_id}: {len(years)} labels but {len(values)} values")
        seen.add(chart_id)
        for year, value in zip(years, values, strict=True):
            rows.append({id_col: chart_id, "year": year, "index_value": value})
    missing = sorted(set(chart_ids) - seen)
    if missing:
        raise RuntimeError(f"AJAX response omitted {len(missing)} chart ids: {missing[:5]}")
    return rows


def _monitoring_rows(page_text: str) -> list[dict[str, Any]]:
    root = html.fromstring(page_text)
    rows: list[dict[str, Any]] = []
    windows = root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " fancybox_window ")]')
    for window in windows:
        country_nodes = window.xpath(".//h2[1]")
        if not country_nodes:
            continue
        country = _text(country_nodes[0])
        country_code = window.get("data-code")
        map_status = window.get("data-color")
        tables = window.xpath('.//table[contains(@class, "map__eu__popup__table")]')
        if not tables:
            rows.append(
                {
                    "country_code": country_code,
                    "country": country,
                    "scheme_index": 0,
                    "scheme_name": None,
                    "map_status": map_status,
                    "website": None,
                    "organisation": None,
                    "status": "no bird monitoring scheme",
                    "start_year": None,
                    "number_of_fieldworkers": None,
                    "species_count": None,
                    "habitats_record": None,
                    "methods": None,
                    "selection_of_plots": None,
                    "sustainable_support": None,
                    "reference": None,
                    "contact": None,
                    "note": None,
                }
            )
            continue
        for idx, table in enumerate(tables, start=1):
            header = table.xpath(".//thead/tr[1]/th")
            scheme_name = _text(header[1]) if len(header) >= 2 else None
            fields = {}
            for tr in table.xpath(".//tbody/tr"):
                cells = tr.xpath("./td")
                if len(cells) < 2:
                    continue
                key = _text(cells[0]).rstrip(":").lower().replace(" ", "_")
                fields[key] = _text(cells[1]) or None
            rows.append(
                {
                    "country_code": country_code,
                    "country": country,
                    "scheme_index": idx,
                    "scheme_name": scheme_name,
                    "map_status": map_status,
                    "website": fields.get("website"),
                    "organisation": fields.get("organisation"),
                    "status": fields.get("status"),
                    "start_year": _int_or_none(fields.get("start")),
                    "number_of_fieldworkers": _int_or_none(fields.get("number_of_fieldworkers")),
                    "species_count": _int_or_none(fields.get("species")),
                    "habitats_record": fields.get("habitats_record"),
                    "methods": fields.get("methods"),
                    "selection_of_plots": fields.get("selection_of_plots"),
                    "sustainable_support": fields.get("sustainable_support"),
                    "reference": fields.get("reference"),
                    "contact": fields.get("contact"),
                    "note": fields.get("note"),
                }
            )
    return rows


def _save(rows: list[dict[str, Any]], asset_id: str, schema: pa.Schema) -> None:
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset_id)


SPECIES_SCHEMA = pa.schema(
    [
        ("species_id", pa.string()),
        ("species_name", pa.string()),
        ("long_term_trend_percent", pa.int64()),
        ("long_term_slope", pa.float64()),
        ("long_term_slope_se", pa.float64()),
        ("ten_year_trend_percent", pa.int64()),
        ("ten_year_slope", pa.float64()),
        ("ten_year_slope_se", pa.float64()),
        ("habitat", pa.string()),
    ]
)

SPECIES_VALUES_SCHEMA = pa.schema(
    [
        ("species_id", pa.string()),
        ("year", pa.int64()),
        ("index_value", pa.float64()),
    ]
)

INDICATORS_SCHEMA = pa.schema(
    [
        ("indicator_id", pa.string()),
        ("indicator_name", pa.string()),
        ("indicator_group", pa.string()),
        ("region", pa.string()),
        ("time_period", pa.string()),
        ("species_count", pa.int64()),
        ("trend_percent", pa.int64()),
    ]
)

INDICATOR_VALUES_SCHEMA = pa.schema(
    [
        ("indicator_id", pa.string()),
        ("year", pa.int64()),
        ("index_value", pa.float64()),
    ]
)

MONITORING_SCHEMA = pa.schema(
    [
        ("country_code", pa.string()),
        ("country", pa.string()),
        ("scheme_index", pa.int64()),
        ("scheme_name", pa.string()),
        ("map_status", pa.string()),
        ("website", pa.string()),
        ("organisation", pa.string()),
        ("status", pa.string()),
        ("start_year", pa.int64()),
        ("number_of_fieldworkers", pa.int64()),
        ("species_count", pa.int64()),
        ("habitats_record", pa.string()),
        ("methods", pa.string()),
        ("selection_of_plots", pa.string()),
        ("sustainable_support", pa.string()),
        ("reference", pa.string()),
        ("contact", pa.string()),
        ("note", pa.string()),
    ]
)


def fetch_species(asset_id: str) -> None:
    _save(_species_rows(_page(SPECIES_URL)), asset_id, SPECIES_SCHEMA)


def fetch_species_values(asset_id: str) -> None:
    page_text = _page(SPECIES_URL)
    species_ids = [row["species_id"] for row in _species_rows(page_text)]
    rows = _chart_rows(page_text, species_ids, "wpj_load_birds", "species_id")
    _save(rows, asset_id, SPECIES_VALUES_SCHEMA)


def fetch_indicators(asset_id: str) -> None:
    _save(_indicator_rows(_page(INDICATORS_URL)), asset_id, INDICATORS_SCHEMA)


def fetch_indicator_values(asset_id: str) -> None:
    page_text = _page(INDICATORS_URL)
    indicator_ids = [row["indicator_id"] for row in _indicator_rows(page_text)]
    rows = _chart_rows(page_text, indicator_ids, "wpj_load_indicators", "indicator_id")
    _save(rows, asset_id, INDICATOR_VALUES_SCHEMA)


def fetch_monitoring_schemes(asset_id: str) -> None:
    _save(_monitoring_rows(_page(HOME_URL)), asset_id, MONITORING_SCHEMA)


DOWNLOAD_SPECS = [
    NodeSpec(id="pecbms-indicator-values", fn=fetch_indicator_values),
    NodeSpec(id="pecbms-indicators", fn=fetch_indicators),
    NodeSpec(id="pecbms-monitoring-schemes", fn=fetch_monitoring_schemes),
    NodeSpec(id="pecbms-species", fn=fetch_species),
    NodeSpec(id="pecbms-species-values", fn=fetch_species_values),
]
