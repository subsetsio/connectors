"""NBS Tanzania — SDG indicator time-series (Goal Tracker platform).

Mechanism: goaltracker_sdg. The site is a Next.js SSG app; the entire corpus
lives behind one build-id-stamped _next/data URL. The build id changes on every
redeploy, so each run resolves it fresh from the page HTML, then fetches a single
goals JSON (any area/goal pair returns the WHOLE corpus: both areas, all
goals/targets/indicators with per-indicator time-series). One ~1.5MB request.

Stateless full re-pull: the corpus is tiny, so every run re-fetches and overwrites.
No incremental query is supported by the source. Two download nodes
(`indicators`, `values`) each re-derive their slice from the same corpus fetch.
"""

import json
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://tanzaniagoaltrack.nbs.go.tz"

INDICATORS_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("area", pa.string()),
    ("description", pa.string()),
    ("type", pa.string()),
    ("frequency", pa.string()),
    ("is_reported", pa.bool_()),
    ("sources", pa.string()),
    ("providers", pa.string()),
    ("definition", pa.string()),
    ("method_of_computation", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("area", pa.string()),
    ("year", pa.int32()),
    ("value", pa.string()),          # raw; transform TRY_CASTs to DOUBLE
    ("unit", pa.string()),
    ("disaggregation", pa.string()),
])


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_corpus() -> dict:
    """Return the corpus dict: {area: {framework: {indicators, goals, ...}}}."""
    html = _get_text(f"{BASE}/platform/tanzania/")
    m = re.search(r'"buildId":"([^"]+)"', html)
    if not m:
        raise RuntimeError("could not locate Next.js buildId in Goal Tracker HTML")
    build_id = m.group(1)
    url = (
        f"{BASE}/_next/data/{build_id}"
        "/platform/tanzania/goals/mainland/1.json?area=mainland&goal=1"
    )
    payload = _get_json(url)
    return payload["pageProps"]["data"]


def _join_list(v) -> str:
    if isinstance(v, list):
        return "; ".join(str(x) for x in v if x is not None)
    return "" if v is None else str(v)


def _disaggregation_label(series: dict) -> str:
    pairs = series.get("disaggregations") or []
    items = sorted(
        ((str(d.get("type")), str(d.get("value"))) for d in pairs),
        key=lambda t: (t[0], t[1]),
    )
    return " | ".join(f"{t}={v}" for t, v in items)


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    data = _fetch_corpus()
    rows = []
    for area in sorted(data.keys()):
        sdg = data[area].get("sdg", {})
        for ind in sdg.get("indicators", []):
            rows.append({
                "indicator_id": str(ind.get("id")) if ind.get("id") is not None else None,
                "area": area,
                "description": ind.get("description"),
                "type": ind.get("type"),
                "frequency": ind.get("frequency"),
                "is_reported": bool(ind.get("isReported")),
                "sources": _join_list(ind.get("sources")),
                "providers": _join_list(ind.get("providers")),
                "definition": ind.get("definition"),
                "method_of_computation": ind.get("methodOfComputation"),
            })
    table = pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_values(node_id: str) -> None:
    asset = node_id
    data = _fetch_corpus()
    seen = {}  # (indicator_id, area, year, disaggregation) -> row; keep first
    for area in sorted(data.keys()):
        sdg = data[area].get("sdg", {})
        for ind in sdg.get("indicators", []):
            iid = str(ind.get("id")) if ind.get("id") is not None else None
            for series in (ind.get("data") or []):
                label = _disaggregation_label(series)
                for ykey, obs in (series.get("data") or {}).items():
                    if not isinstance(obs, dict):
                        continue
                    yr = obs.get("year")
                    if not isinstance(yr, int):
                        try:
                            yr = int(str(ykey))
                        except (TypeError, ValueError):
                            continue
                    val = obs.get("value")
                    val_str = None if val is None else str(val)
                    key = (iid, area, yr, label)
                    existing = seen.get(key)
                    if existing is not None:
                        # prefer a row that carries a value over a null one
                        if existing["value"] is not None or val_str is None:
                            continue
                    seen[key] = {
                        "indicator_id": iid,
                        "area": area,
                        "year": yr,
                        "value": val_str,
                        "unit": obs.get("unit"),
                        "disaggregation": label,
                    }
    rows = list(seen.values())
    table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nbs-tanzania-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="nbs-tanzania-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nbs-tanzania-indicators-transform",
        deps=["nbs-tanzania-indicators"],
        sql='''
            SELECT
                indicator_id,
                area,
                description,
                type,
                frequency,
                is_reported,
                sources,
                providers,
                definition,
                method_of_computation
            FROM "nbs-tanzania-indicators"
            WHERE indicator_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="nbs-tanzania-values-transform",
        deps=["nbs-tanzania-values"],
        sql='''
            SELECT
                indicator_id,
                area,
                CAST(year AS INTEGER)       AS year,
                TRY_CAST(value AS DOUBLE)   AS value,
                unit,
                disaggregation
            FROM "nbs-tanzania-values"
            WHERE indicator_id IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
