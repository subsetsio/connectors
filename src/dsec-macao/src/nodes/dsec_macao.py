"""DSEC Macao (Statistics and Census Service) — Time Series Database connector.

Mechanism: rest_timeseries (the JSON backend of https://www.dsec.gov.mo/ts/).

Two subsets, both stateless full re-pulls (the whole corpus is small enough to
re-fetch every run in a few minutes, and the API exposes no incremental/since
filter — each refresh picks up revisions for free):

  dsec-macao-indicators : reference catalog of every tree node (~9896 nodes,
                          ~7911 leaf indicators). Walk GET /Indicatorv3 (20
                          roots) then GET /Indicatorv3/{id} for each non-leaf.
  dsec-macao-values     : long-format VAL observations for every leaf indicator.
                          Fetched per period-type (Yearly/Quarterly/Monthly/
                          ThreeConsecutiveMonths) in batches via
                          POST /IndicatorValue/LatestSameEndPeriodv3.

API quirks (verified by probing): success returns HTTP 201 with a
{Debug_msg, Value, Status:'OK'|'ERROR'} envelope; `types` must be a JSON array
the same length as `indicator_ids` (one per id) or the server throws
ArgumentOutOfRange; `dataPeriods` as a single-element array broadcasts across
the batch; requesting a period an indicator lacks returns null-padded rows
(filtered out here), so we fetch ONE period-type per call to keep PeriodID
unambiguous between quarterly and monthly.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    post,
    save_raw_parquet,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://www.dsec.gov.mo/TimeSeriesApi/App"
ROOT_URL = f"{BASE}/Indicatorv3"
VALUE_URL = f"{BASE}/IndicatorValue/LatestSameEndPeriodv3"
SOURCE_MIN_YEAR = 1900  # earliest plausible; server clamps to what exists
WALK_WORKERS = 16
FETCH_WORKERS = 8
BATCH_SIZE = 40
FLUSH_ROWS = 100_000

# (availability flag on a node, dataPeriods value sent to the value endpoint)
PERIOD_TYPES = [
    ("YearlyAvailable", "Yearly"),
    ("QuarterlyAvailable", "Quarterly"),
    ("MonthlyAvailable", "Monthly"),
    ("ThreeConsecutiveMonthsAvaliable", "ThreeConsecutiveMonths"),
]

INDICATORS_SCHEMA = pa.schema([
    ("indicator_id", pa.int64()),
    ("parent_id", pa.int64()),
    ("indicator_id_path", pa.string()),
    ("is_leaf", pa.bool_()),
    ("global_order", pa.string()),
    ("name_en", pa.string()),
    ("name_pt", pa.string()),
    ("name_zh_mo", pa.string()),
    ("name_zh_cn", pa.string()),
    ("unit_en", pa.string()),
    ("unit_pt", pa.string()),
    ("unit_zh_mo", pa.string()),
    ("min_year", pa.int32()),
    ("max_year", pa.int32()),
    ("yearly_available", pa.bool_()),
    ("quarterly_available", pa.bool_()),
    ("monthly_available", pa.bool_()),
    ("three_consec_months_available", pa.bool_()),
    ("val_available", pa.bool_()),
    ("spv_available", pa.bool_()),
    ("ppv_available", pa.bool_()),
    ("pot_available", pa.bool_()),
])

VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.int64()),
    ("data_period", pa.string()),
    ("year", pa.int32()),
    ("period_id", pa.int32()),
    ("reference_period", pa.string()),
    ("function_type", pa.string()),
    ("value", pa.float64()),
    ("unit", pa.string()),
    ("last_update_date", pa.string()),
])


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_value(url):
    """GET a /Indicatorv3 node; return its `Value` list (raise on ERROR)."""
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("Status") != "OK":
        raise RuntimeError(f"{url}: {payload.get('Debug_msg')!r}")
    return payload.get("Value") or []


@transient_retry()
def _post_values(indicator_ids, data_period, to_year):
    body = {
        "indicator_ids": [str(i) for i in indicator_ids],
        "language": "en-us",
        "types": ["VAL"] * len(indicator_ids),
        "dataPeriods": [data_period],
        "fromYear": SOURCE_MIN_YEAR,
        "toYear": to_year,
    }
    resp = post(VALUE_URL, json=body, timeout=(10.0, 180.0))
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("Status") != "OK":
        raise RuntimeError(
            f"values {data_period} ids={indicator_ids[:3]}...: {payload.get('Debug_msg')!r}"
        )
    return payload.get("Value") or []


# --------------------------------------------------------------------------- #
# Catalog tree walk (shared by both nodes; each runs in its own process)
# --------------------------------------------------------------------------- #
def _walk_tree():
    """BFS the indicator tree. Returns {indicator_id: node_dict}."""
    nodes = {}
    roots = _get_value(ROOT_URL)
    for n in roots:
        nodes[int(n["IndicatorID"])] = n
    frontier = [int(n["IndicatorID"]) for n in roots if n.get("IsLeafNode") != "True"]
    rounds = 0
    while frontier:
        rounds += 1
        if rounds > 50:  # safety ceiling: the tree is ~10 levels deep
            raise RuntimeError(f"tree walk exceeded 50 levels (cycle?); known={len(nodes)}")
        with ThreadPoolExecutor(max_workers=WALK_WORKERS) as ex:
            results = list(ex.map(lambda i: _get_value(f"{ROOT_URL}/{i}"), frontier))
        nxt = []
        for children in results:
            for c in children:
                cid = int(c["IndicatorID"])
                if cid not in nodes:
                    nodes[cid] = c
                    if c.get("IsLeafNode") != "True":
                        nxt.append(cid)
        frontier = nxt
    return nodes


def _as_bool(v):
    return str(v).strip().lower() == "true"


def _as_int(v):
    # The API returns numeric ids as JSON floats (e.g. Parent=9001.0) and years
    # as strings ("2002"); int(float(...)) handles both, int("9001.0") would not.
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# Download node: indicators catalog
# --------------------------------------------------------------------------- #
def fetch_indicators(node_id: str) -> None:
    asset = node_id
    nodes = _walk_tree()
    rows = []
    for n in nodes.values():
        rows.append({
            "indicator_id": int(n["IndicatorID"]),
            "parent_id": _as_int(n.get("Parent")) or 0,
            "indicator_id_path": n.get("indicatorIdPath"),
            "is_leaf": _as_bool(n.get("IsLeafNode")),
            "global_order": n.get("GlobalOrder"),
            "name_en": n.get("DescriptionEngl"),
            "name_pt": n.get("DescriptionPort"),
            "name_zh_mo": n.get("Description"),
            "name_zh_cn": n.get("DescriptionSimplifiedChinese"),
            "unit_en": n.get("UnitLabelEngl"),
            "unit_pt": n.get("UnitLabelPort"),
            "unit_zh_mo": n.get("UnitLabel"),
            "min_year": _as_int(n.get("minYear")),
            "max_year": _as_int(n.get("maxYear")),
            "yearly_available": _as_bool(n.get("YearlyAvailable")),
            "quarterly_available": _as_bool(n.get("QuarterlyAvailable")),
            "monthly_available": _as_bool(n.get("MonthlyAvailable")),
            "three_consec_months_available": _as_bool(n.get("ThreeConsecutiveMonthsAvaliable")),
            "val_available": _as_bool(n.get("VALAvailable")),
            "spv_available": _as_bool(n.get("SPVAvailable")),
            "ppv_available": _as_bool(n.get("PPVAvailable")),
            "pot_available": _as_bool(n.get("POTAvailable")),
        })
    table = pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# Download node: long-format values
# --------------------------------------------------------------------------- #
def _rows_from_response(value, data_period):
    out = []
    for ind in value:
        iid = int(ind["indicatorId"])
        for r in ind.get("dsecIndicatorData") or []:
            val = r.get("IndicatorValue")
            if val is None:
                continue
            out.append({
                "indicator_id": iid,
                "data_period": data_period,
                "year": _as_int(r.get("Year")),
                "period_id": _as_int(r.get("PeriodID")),
                "reference_period": r.get("ReferencePeriod"),
                "function_type": r.get("type") or "VAL",
                "value": float(val),
                "unit": r.get("UnitLabel"),
                "last_update_date": r.get("LastUpdateDate"),
            })
    return out


def fetch_values(node_id: str) -> None:
    asset = node_id
    to_year = datetime.now(tz=timezone.utc).year + 1
    nodes = _walk_tree()
    leaves = [n for n in nodes.values()
              if n.get("IsLeafNode") == "True" and _as_bool(n.get("VALAvailable"))]

    buf = []
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        def flush(force=False):
            nonlocal buf
            if buf and (force or len(buf) >= FLUSH_ROWS):
                writer.write_table(pa.Table.from_pylist(buf, schema=VALUES_SCHEMA))
                buf = []

        for flag, data_period in PERIOD_TYPES:
            ids = [int(n["IndicatorID"]) for n in leaves if _as_bool(n.get(flag))]
            batches = [ids[i:i + BATCH_SIZE] for i in range(0, len(ids), BATCH_SIZE)]
            if not batches:
                continue
            with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as ex:
                for value in ex.map(lambda b: _post_values(b, data_period, to_year), batches):
                    buf.extend(_rows_from_response(value, data_period))
                    flush()
        flush(force=True)


DOWNLOAD_SPECS = [
    NodeSpec(id="dsec-macao-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="dsec-macao-values", fn=fetch_values, kind="download"),
]
