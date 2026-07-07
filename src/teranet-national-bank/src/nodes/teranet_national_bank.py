"""Teranet-National Bank House Price Index downloads.

The source publishes static files behind the public visualizer. We normalize
the visualizer JSON into two SQL-readable raw parquet assets: monthly
observations and index/profile metadata.
"""
from __future__ import annotations

from datetime import date

import httpx
import pyarrow as pa

from subsets_utils import MaintainSpec, NodeSpec, raw_asset_exists, save_raw_parquet

SLUG = "teranet-national-bank"
DATA_URL = "https://housepriceindex.ca/_data/indx_data.json"
CONNECT_TIMEOUT = 20.0
READ_TIMEOUT = 120.0

OBSERVATION_SCHEMA = pa.schema(
    [
        ("index_id", pa.string()),
        ("period", pa.date32()),
        ("index_value", pa.float64()),
        ("index_change_12m_pct", pa.float64()),
        ("sa_index_value", pa.float64()),
        ("sa_index_change_12m_pct", pa.float64()),
        ("sales_pair_count", pa.float64()),
        ("sales_pair_count_change_12m_pct", pa.float64()),
    ]
)

SERIES_SCHEMA = pa.schema(
    [
        ("index_id", pa.string()),
        ("type", pa.string()),
        ("name", pa.string()),
        ("name_fr", pa.string()),
        ("map_left", pa.int64()),
        ("map_top", pa.int64()),
        ("map_class", pa.string()),
        ("c11_weight", pa.float64()),
        ("mc_weight", pa.float64()),
        ("updates", pa.string()),
        ("latest_index_value", pa.float64()),
        ("latest_month_change_pct", pa.float64()),
        ("latest_ytd_change_pct", pa.float64()),
        ("latest_yoy_change_pct", pa.float64()),
        ("latest_from_peak_pct", pa.float64()),
        ("index_peak_date", pa.string()),
        ("population", pa.int64()),
        ("land_sq_km", pa.float64()),
        ("population_density", pa.float64()),
        ("occupied_private_dwellings", pa.int64()),
        ("owned_rented", pa.string()),
        ("one_family_households", pa.int64()),
        ("multi_family_households", pa.int64()),
        ("non_family_households", pa.int64()),
        ("avg_household_income", pa.int64()),
        ("aggregate_dwelling_value", pa.float64()),
        ("description_en", pa.string()),
        ("description_fr", pa.string()),
    ]
)


def _fetch_data() -> dict:
    # The site certificate chain fails in the connector venv's CA store. Keep
    # this exception local to this source rather than changing shared runtime.
    with httpx.Client(
        follow_redirects=True,
        verify=False,
        headers={"User-Agent": "DataIntegrations/1.0"},
        timeout=httpx.Timeout(READ_TIMEOUT, connect=CONNECT_TIMEOUT),
    ) as client:
        response = client.get(DATA_URL)
        response.raise_for_status()
        return response.json()


def _month_offset(start: date, offset: int) -> date:
    month0 = start.year * 12 + (start.month - 1) + offset
    return date(month0 // 12, month0 % 12 + 1, 1)


def _float_or_none(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int_or_none(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _series_value(block: dict, index_id: str, pos: int) -> float | None:
    values = block.get(index_id) or []
    if pos >= len(values):
        return None
    return _float_or_none(values[pos])


def fetch_hpi_observations(node_id: str) -> None:
    payload = _fetch_data()
    data = payload["data"]
    start = date.fromisoformat(data["meta"]["start_date"])
    series_ids = sorted(data["indx"])

    rows = []
    for index_id in series_ids:
        series_len = len(data["indx"][index_id])
        for pos in range(series_len):
            rows.append(
                {
                    "index_id": index_id,
                    "period": _month_offset(start, pos),
                    "index_value": _series_value(data.get("indx", {}), index_id, pos),
                    "index_change_12m_pct": _series_value(data.get("indx_ch", {}), index_id, pos),
                    "sa_index_value": _series_value(data.get("sa_indx", {}), index_id, pos),
                    "sa_index_change_12m_pct": _series_value(data.get("sa_indx_ch", {}), index_id, pos),
                    "sales_pair_count": _series_value(data.get("spc", {}), index_id, pos),
                    "sales_pair_count_change_12m_pct": _series_value(data.get("spc_ch", {}), index_id, pos),
                }
            )

    table = pa.Table.from_pylist(rows, schema=OBSERVATION_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_hpi_series(node_id: str) -> None:
    payload = _fetch_data()
    rows = []
    for index_id, profile in sorted(payload["profiles"].items()):
        rows.append(
            {
                "index_id": index_id,
                "type": profile.get("type"),
                "name": profile.get("name"),
                "name_fr": profile.get("name_fr"),
                "map_left": _int_or_none(profile.get("map_left")),
                "map_top": _int_or_none(profile.get("map_top")),
                "map_class": profile.get("map_class"),
                "c11_weight": _float_or_none(profile.get("c11_weight")),
                "mc_weight": _float_or_none(profile.get("mc_weight")),
                "updates": profile.get("updates"),
                "latest_index_value": _float_or_none(profile.get("indx_value")),
                "latest_month_change_pct": _float_or_none(profile.get("indx_mom")),
                "latest_ytd_change_pct": _float_or_none(profile.get("indx_ytd")),
                "latest_yoy_change_pct": _float_or_none(profile.get("indx_yoy")),
                "latest_from_peak_pct": _float_or_none(profile.get("indx_from_peak")),
                "index_peak_date": profile.get("indx_peak_date"),
                "population": _int_or_none(profile.get("population")),
                "land_sq_km": _float_or_none(profile.get("land_in_sq_km")),
                "population_density": _float_or_none(profile.get("pop_density")),
                "occupied_private_dwellings": _int_or_none(profile.get("occ_priv_dwellings")),
                "owned_rented": profile.get("owned_rented"),
                "one_family_households": _int_or_none(profile.get("one_family_hh")),
                "multi_family_households": _int_or_none(profile.get("multi_family_hh")),
                "non_family_households": _int_or_none(profile.get("non_family_hh")),
                "avg_household_income": _int_or_none(profile.get("avg_hh_income")),
                "aggregate_dwelling_value": _float_or_none(profile.get("agg_value_of_dwellings")),
                "description_en": profile.get("description_en"),
                "description_fr": profile.get("description_fr"),
            }
        )

    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="teranet-national-bank-hpi-observations",
        fn=fetch_hpi_observations,
    ),
    NodeSpec(
        id="teranet-national-bank-hpi-series",
        fn=fetch_hpi_series,
    ),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="teranet-national-bank-hpi-observations",
        description="Updated monthly per https://housepriceindex.ca/ download data vintage; refetch if raw is older than 45 days.",
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=45),
    ),
    MaintainSpec(
        asset_id="teranet-national-bank-hpi-series",
        description="Updated monthly with the HPI visualizer payload; refetch if raw is older than 45 days.",
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=45),
    ),
]
