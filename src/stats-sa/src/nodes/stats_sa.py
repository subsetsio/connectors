from __future__ import annotations

import re
from datetime import UTC, datetime
from urllib.parse import urlparse

from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, save_raw_ndjson


SPEC_PRODUCTS = "stats-sa-time-series-products"
SPEC_VALUES = "stats-sa-time-series-values"
ISIBALO_DATA_ROOT = "https://isibaloweb.statssa.gov.za/data/ETS"

HEADER_LABELS = {
    "H01": "release_no",
    "H02": "series_name",
    "H03": "variable_name",
    "H04": "description_1",
    "H05": "description_2",
    "H06": "description_3",
    "H07": "description_4",
    "H08": "description_5",
    "H09": "description_6",
    "H10": "description_7",
    "H11": "description_8",
    "H12": "description_9",
    "H13": "area_1",
    "H14": "area_2",
    "H15": "constant",
    "H16": "seasonal",
    "H17": "unit",
    "H18": "base",
    "H19": "reserved_1",
    "H20": "reserved_2",
    "H21": "reserved_3",
    "H22": "reserved_4",
    "H23": "release_date",
    "H24": "start_date",
    "H25": "frequency",
}

PRODUCTS = [
    {
        "product_id": "manufacturing-production-and-sales",
        "title": "Manufacturing Production and Sales",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Manufacturing%20Production%20and%20Sales/manufacture.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Manufacturing%20Production%20and%20SalesP3041_2/P3041_2p.json",
        ],
    },
    {
        "product_id": "electricity-generated",
        "title": "Electricity Generated",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Electricity%20Generated/electricity.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Electricity%20GeneratedP4141/P41412000p.json",
            f"{ISIBALO_DATA_ROOT}/Monthly/Electricity%20GeneratedP4141/P41411990p.json",
            f"{ISIBALO_DATA_ROOT}/Monthly/Electricity%20GeneratedP4141/P41411985p.json",
        ],
    },
    {
        "product_id": "mining-production-and-sales",
        "title": "Mining Production and Sales",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Mining%20Production%20and%20Sales/mining_monthly.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Mining%20Production%20and%20SalesP2041/P20412003p.json",
            f"{ISIBALO_DATA_ROOT}/Monthly/Mining%20Production%20and%20SalesP2041/P20411980p.json",
        ],
    },
    {
        "product_id": "wholesale-trade-sales",
        "title": "Wholesale Trade Sales",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Wholesale%20Trade%20Sales/wholesale.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Wholesale%20Trade%20SalesP6141_2/P6141_21998p.json",
        ],
    },
    {
        "product_id": "land-transport",
        "title": "Land Transport",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Land%20Transport/transport.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Land%20TransportP7162/P7162p.json",
        ],
    },
    {
        "product_id": "civil-cases-for-debt",
        "title": "Civil Cases of Debt",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Civil%20Cases%20for%20Debt/civil.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Civil%20Cases%20for%20DebtP0041/P00412000p.json",
            f"{ISIBALO_DATA_ROOT}/Monthly/Civil%20Cases%20for%20DebtP0041/P00411999p.json",
            f"{ISIBALO_DATA_ROOT}/Monthly/Civil%20Cases%20for%20DebtP0041/P00411989p.json",
        ],
    },
    {
        "product_id": "liquidations-and-insolvencies",
        "title": "Liquidations and Insolvencies",
        "frequency": "Monthly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/monthly/Liquidations%20and%20Insolvencies/liquid.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Monthly/Liquidations%20and%20InsolvenciesP0043_1/P0043_1p.json",
        ],
    },
    {
        "product_id": "manufacturing-utilisation-of-production-capacity",
        "title": "Manufacturing: Utilisation of production capacity",
        "frequency": "Quarterly",
        "landing_url": "https://isibaloweb.statssa.gov.za/pages/surveys/ets/quarterly/Utilisation/utilisation.php",
        "json_urls": [
            f"{ISIBALO_DATA_ROOT}/Quarterly/Manufacturing%20Utilisation%20of%20Production%20CapacityP3043/P3043p.json",
        ],
    },
]


def _assert_not_interstitial(text: str, url: str) -> None:
    lowered = text.lower()
    if "incapsula" in lowered or "_incapsula_resource" in lowered:
        raise RuntimeError(f"Stats SA returned Incapsula interstitial for {url}")


def _fetch_json(url: str) -> dict:
    response = get(url, timeout=120.0)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "html" in content_type.lower():
        _assert_not_interstitial(response.text, url)
        raise RuntimeError(f"Stats SA returned HTML instead of JSON for {url}")
    return response.json()


def _table_items(document: dict, url: str) -> tuple[str, list[dict]]:
    for key, value in document.items():
        if key.startswith("SASTableData+") and isinstance(value, list):
            return key, value
    raise RuntimeError(f"Stats SA JSON did not contain a SASTableData table for {url}")


def _period_from_code(code: str) -> tuple[str | None, str | None]:
    if match := re.fullmatch(r"MO(\d{2})(\d{4})", code):
        month, year = match.groups()
        return f"{year}-{month}-01", "monthly"
    if match := re.fullmatch(r"Q(?:R)?(\d{2}|\d)(\d{4})", code):
        quarter, year = match.groups()
        return f"{year}-Q{int(quarter)}", "quarterly"
    if match := re.fullmatch(r"YR(\d{4})", code):
        (year,) = match.groups()
        return year, "annual"
    return None, None


def _numeric_value(value: object) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if not text or text in {"-", ".."}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def fetch_products(node_id: str) -> None:
    fetched_at = datetime.now(UTC).isoformat()
    rows = [
        {
            "product_id": product["product_id"],
            "title": product["title"],
            "frequency": product["frequency"],
            "landing_url": product["landing_url"],
            "json_file_count": len(product["json_urls"]),
            "json_urls": product["json_urls"],
            "fetched_at": fetched_at,
        }
        for product in PRODUCTS
    ]
    save_raw_ndjson(rows, node_id)


def _records_for_product(product: dict, fetched_at: str) -> list[dict]:
    rows = []
    for url in product["json_urls"]:
        document = _fetch_json(url)
        table_name, records = _table_items(document, url)
        source_file = urlparse(url).path.rsplit("/", 1)[-1]
        for source_row_number, record in enumerate(records, start=1):
            header = {HEADER_LABELS[key]: record.get(key) for key in HEADER_LABELS}
            variable_name = str(record.get("H03") or "").strip()
            for key, value in record.items():
                period, period_frequency = _period_from_code(key)
                if period is None:
                    continue
                rows.append(
                    {
                        "product_id": product["product_id"],
                        "product_title": product["title"],
                        "source_url": url,
                        "source_file": source_file,
                        "source_table": table_name,
                        "source_row_number": source_row_number,
                        "series_id": f"{product['product_id']}:{variable_name}",
                        "period_code": key,
                        "period": period,
                        "period_frequency": period_frequency,
                        "value": _numeric_value(value),
                        "value_raw": None if value is None else str(value),
                        "fetched_at": fetched_at,
                        **header,
                    }
                )
    return rows


def fetch_values(node_id: str) -> None:
    fetched_at = datetime.now(UTC).isoformat()
    rows = []
    for product in PRODUCTS:
        rows.extend(_records_for_product(product, fetched_at))
    if not rows:
        raise RuntimeError("Stats SA JSON files contained no time-series observations")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=SPEC_PRODUCTS, fn=fetch_products),
    NodeSpec(id=SPEC_VALUES, fn=fetch_values),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=SPEC_PRODUCTS,
        description="Stats SA ISIbalo economic time-series product list; refreshed weekly (inferred from Stats SA time-series publication pages).",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=7),
    ),
    MaintainSpec(
        asset_id=SPEC_VALUES,
        description="Stats SA ISIbalo economic time-series JSON files; refreshed weekly (inferred from Stats SA time-series publication pages).",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=7),
    ),
]
