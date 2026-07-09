"""CFPB Consumer Credit Trends — monthly series from the Consumer Credit
Information Panel.

One CSV per market/metric under
files.consumerfinance.gov/data/consumer-credit-trends/<market>/. Each entity is
one metric across up to four markets (mortgages MTG, credit-cards CRC, auto-loans
AUT, student-loans STU); we fetch each market, tag rows with `market`, coerce
numerics, and write one NDJSON asset. Metric column sets differ across entities
but are homogeneous within an entity, so a passthrough SQL transform works.
"""

from __future__ import annotations

import csv
import io

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _http_get

_CCT_BASE = "https://files.consumerfinance.gov/data/consumer-credit-trends/"
# market directory -> (filename market code, human label)
_CCT_MARKETS = {
    "mortgages": ("MTG", "Mortgages"),
    "credit-cards": ("CRC", "Credit cards"),
    "auto-loans": ("AUT", "Auto loans"),
    "student-loans": ("STU", "Student loans"),
}
# entity id (node_id minus `cfpb-`) -> file metric prefix (the collect metric_key)
_CCT_METRIC = {
    "cct-crt-data": "crt_data",
    "cct-inq-data": "inq_data",
    "cct-map-data": "map_data",
    "cct-num-data": "num_data",
    "cct-vol-data": "vol_data",
    "cct-volume-data-age-group": "volume_data_Age_Group",
    "cct-volume-data-income-level": "volume_data_Income_Level",
    "cct-volume-data-score-level": "volume_data_Score_Level",
    "cct-yoy-data-age-group": "yoy_data_Age_Group",
    "cct-yoy-data-all": "yoy_data_all",
    "cct-yoy-data-income-level": "yoy_data_Income_Level",
    "cct-yoy-data-score-level": "yoy_data_Score_Level",
}
# Columns that are categorical labels, kept as strings; everything else numeric.
_CCT_STRING_FIELDS = {
    "date", "market", "age_group", "income_level_group",
    "credit_score_group", "state_abbr", "fips_code",
}


def _cct_coerce(key: str, value: str):
    """Type a raw CSV cell: month -> int, label columns -> str, else -> float."""
    if value is None or value == "":
        return None
    if key == "month":
        try:
            return int(value)
        except ValueError:
            return value
    if key in _CCT_STRING_FIELDS:
        return value
    try:
        return float(value)
    except ValueError:
        return value


def fetch_credit_trend(node_id: str) -> None:
    """Fetch one credit-trends metric across all markets it is published for,
    tag each row with its `market`, and write one NDJSON asset (`node_id`).

    A market whose file does not exist for this metric (e.g. student-loans has
    no crt_data/inq_data) returns 404 and is skipped; a WAF block (403) or 5xx
    surfaces loudly. At least one market must yield rows.
    """
    entity = node_id[len("cfpb-"):]
    metric = _CCT_METRIC[entity]

    rows: list[dict] = []
    fetched_markets: list[str] = []
    for directory, (code, label) in _CCT_MARKETS.items():
        url = f"{_CCT_BASE}{directory}/{metric}_{code}.csv"
        resp = _http_get(url, timeout=60)
        if resp.status_code == 404:
            print(f"  {node_id}: {label} not published for {metric} (404), skipping")
            continue
        resp.raise_for_status()
        reader = csv.DictReader(io.StringIO(resp.text))
        n_before = len(rows)
        for record in reader:
            row = {k: _cct_coerce(k, v) for k, v in record.items()}
            row["market"] = label
            rows.append(row)
        fetched_markets.append(label)
        print(f"  {node_id}: {label} -> {len(rows) - n_before} rows")

    if not rows:
        raise ValueError(
            f"{node_id}: no rows for metric {metric!r} across any market "
            f"(markets tried: {list(_CCT_MARKETS)})"
        )
    print(f"  {node_id}: {len(rows):,} rows from markets {fetched_markets}")
    save_raw_ndjson(rows, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="cfpb-cct-crt-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-inq-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-map-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-num-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-vol-data", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-age-group", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-income-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-volume-data-score-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-age-group", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-all", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-income-level", fn=fetch_credit_trend, kind="download"),
    NodeSpec(id="cfpb-cct-yoy-data-score-level", fn=fetch_credit_trend, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=(spec.id,),
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in _DOWNLOAD_SPECS
]
