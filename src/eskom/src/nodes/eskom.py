"""Eskom Data Portal connector.

Every Eskom Data Portal dashboard page embeds a Power BI 'publish to web'
report. There is no bulk/CSV API (the 5-year CSV form is an async, human-only
email flow), so the data is read straight from Power BI's public, no-auth
querydata API — the same calls the embedded viewer makes.

Per entity, the fetch fn:
  1. GETs the dashboard page and extracts the embedded
     ``app.powerbi.com/view?r=<token>`` iframe; base64-decodes the token to the
     report's resourceKey ``k`` (re-extracted every run, so the connector
     self-heals when Eskom re-publishes a report).
  2. GETs ``modelsAndExploration`` (resourceKey header) for the model id,
     dataset name, report id and the report's visual definitions.
  3. For each *data* visual (one with both a grouping column and a measure),
     POSTs the visual's own semantic query to ``querydata`` with a flat
     binding, then reconstructs the delta-/dictionary-encoded DSR rows.
  4. Normalises every report to one uniform long shape —
     ``(period_label, period_ms, series, value)`` — and writes NDJSON.

Each Power BI model holds only a short recent window (yesterday / last 7 days /
weekly / monthly / financial-year, per page), so this is a stateless full
re-pull every run (overwrite); there is no incremental filter to exploit and
the payloads are tiny (low single-digit MBs total).
"""

import base64
import datetime as _dt
import json
import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS, PAGE_PATHS

PORTAL = "https://www.eskom.co.za/dataportal/"
# All Eskom reports live in the same tenant/cluster (token "c":8) → one host.
WABI = "https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
# Cloudflare in front of the portal rejects generic agents; a browser UA passes.
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
# Power BI value type codes seen in the DSR "S" schema rows.
T_DATETIME = 7
# Per-visual row cap. The dashboards expose short windows (≤ a few thousand
# points); hitting this means a model grew unexpectedly and we'd silently
# truncate — so we raise instead.
WINDOW_COUNT = 30000


@transient_retry()
def _get(url, **kw):
    kw.setdefault("timeout", (10.0, 120.0))
    r = get(url, **kw)
    r.raise_for_status()
    return r


@transient_retry()
def _post_json(url, body, headers):
    r = post(url, json=body, headers=headers, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()


def _resource_key(entity_id: str) -> str:
    """Fetch the dashboard page and decode the embedded report resourceKey."""
    page = PORTAL + PAGE_PATHS[entity_id]
    html = _get(page, headers={"User-Agent": BROWSER_UA}).text
    m = re.search(r"app\.powerbi\.com/view\?r=([A-Za-z0-9=_\-]+)", html)
    if not m:
        raise RuntimeError(f"no Power BI embed token found on {page}")
    token = m.group(1)
    decoded = json.loads(base64.b64decode(token + "=" * (-len(token) % 4)).decode())
    rk = decoded.get("k")
    if not rk:
        raise RuntimeError(f"embed token on {page} has no resourceKey")
    return rk


def _models_and_exploration(rk: str) -> dict:
    url = f"{WABI}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true"
    return _get(url, headers={"X-PowerBI-ResourceKey": rk}).json()


def _data_visuals(exploration: dict):
    """Yield prototypeQueries for visuals that carry data (≥1 grouping column
    AND ≥1 aggregated measure) — skips cards, slicers and text boxes."""
    for section in exploration.get("sections", []):
        for vc in section.get("visualContainers", []):
            try:
                cfg = json.loads(vc.get("config", "{}"))
            except (ValueError, TypeError):
                continue
            pq = cfg.get("singleVisual", {}).get("prototypeQuery")
            if not pq:
                continue
            sel = pq.get("Select", [])
            has_group = any("Aggregation" not in s for s in sel)
            has_measure = any("Aggregation" in s for s in sel)
            if has_group and has_measure:
                yield pq


def _query_visual(rk, model, report_id, pq):
    n = len(pq["Select"])
    body = {
        "version": "1.0.0",
        "queries": [{
            "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
                "Query": pq,
                "Binding": {
                    "Primary": {"Groupings": [{"Projections": list(range(n))}]},
                    "DataReduction": {"DataVolume": 4,
                                      "Primary": {"Window": {"Count": WINDOW_COUNT}}},
                    "Version": 1,
                },
            }}]},
            "QueryId": "",
            "ApplicationContext": {"DatasetId": model["dbName"],
                                   "Sources": [{"ReportId": report_id}]},
        }],
        "cancelQueries": [],
        "modelId": model["id"],
    }
    headers = {"X-PowerBI-ResourceKey": rk, "Content-Type": "application/json"}
    res = _post_json(f"{WABI}/public/reports/querydata?synchronous=true", body, headers)
    return res["results"][0]["result"]["data"]


def _decode_dsr(data: dict):
    """Reconstruct Power BI DSR rows: carry-forward repeat bitmask (R), null
    bitmask (Ø) and ValueDicts (DN) dictionary indices. Returns
    (column_names, type_codes, dict_names, rows-as-resolved-lists)."""
    select = data.get("descriptor", {}).get("Select", [])
    names = [s.get("Name", "") for s in select]
    ds = data["dsr"]["DS"][0]
    dm = ds["PH"][0]["DM0"]
    schema = next((x["S"] for x in dm if "S" in x), None)
    if schema is None:
        return names, [], [], []
    ncols = len(schema)
    types = [s.get("T") for s in schema]
    dnames = [s.get("DN") for s in schema]
    dicts = ds.get("ValueDicts", {})

    rows = []
    prev = [None] * ncols
    for item in dm:
        if "S" in item:
            continue
        c = item.get("C", [])
        repeat = item.get("R", 0)
        nulls = item.get("Ø", 0)  # "Ø"
        raw = []
        ci = 0
        for i in range(ncols):
            bit = 1 << i
            if repeat & bit:
                raw.append(prev[i])
            elif nulls & bit:
                raw.append(None)
            else:
                raw.append(c[ci])
                ci += 1
        prev = raw[:]
        resolved = []
        for i in range(ncols):
            v = raw[i]
            if v is not None and dnames[i] and isinstance(v, int):
                d = dicts.get(dnames[i])
                if d is not None and 0 <= v < len(d):
                    v = d[v]
            resolved.append(v)
        rows.append(resolved)
    return names, types, dnames, rows


_AGG_RE = re.compile(r"^[A-Za-z]+\((.*)\)$")


def _clean_series(name: str) -> str:
    inner = name
    m = _AGG_RE.match(name)
    if m:
        inner = m.group(1)
    return inner.split(".")[-1].strip() or name


def _to_float(v):
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _iso(ms) -> str:
    return _dt.datetime.fromtimestamp(ms / 1000, tz=_dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def _rows_from_visual(data: dict):
    """Turn one decoded visual into long rows keyed (period_label, period_ms,
    series, value). Drops rows that cannot be placed (null time axis / null
    value)."""
    names, types, dnames, rows = _decode_dsr(data)
    if not rows:
        return []
    ncols = len(types)
    sel = data.get("descriptor", {}).get("Select", [])
    # group columns = non-aggregation selects; measures = aggregation selects.
    is_measure = ["Aggregation" in s for s in sel] + [False] * (ncols - len(sel))
    group_idx = [i for i in range(ncols) if not is_measure[i]]
    measure_idx = [i for i in range(ncols) if is_measure[i]]
    time_idx = next((i for i in group_idx if types[i] == T_DATETIME), None)
    cat_idx = [i for i in group_idx if i != time_idx]

    out = []
    for row in rows:
        period_ms = None
        parts = []
        if time_idx is not None:
            tv = row[time_idx]
            if tv is None:  # has a time axis but this row isn't on it → drop
                continue
            try:
                period_ms = int(tv)
                parts.append(_iso(period_ms))
            except (TypeError, ValueError):
                period_ms = None
                parts.append(str(tv))
        for i in cat_idx:
            if row[i] is not None:
                parts.append(str(row[i]))
        period_label = " | ".join(parts) if parts else None
        if period_label is None:
            continue
        for i in measure_idx:
            value = _to_float(row[i])
            if value is None:
                continue
            out.append({
                "period_label": period_label,
                "period_ms": period_ms,
                "series": _clean_series(names[i]) if i < len(names) else f"col{i}",
                "value": value,
            })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len("eskom-"):]
    rk = _resource_key(entity_id)
    me = _models_and_exploration(rk)
    if not me.get("models"):
        raise RuntimeError(f"{entity_id}: report {rk} exposes no model")
    model = me["models"][0]
    exploration = me["exploration"]
    report_id = exploration.get("reportId")

    merged = {}
    visual_count = 0
    for pq in _data_visuals(exploration):
        visual_count += 1
        data = _query_visual(rk, model, report_id, pq)
        produced = _rows_from_visual(data)
        if len(produced) >= WINDOW_COUNT:
            raise RuntimeError(
                f"{entity_id}: visual returned {len(produced)} rows (>= cap "
                f"{WINDOW_COUNT}); model grew — raise WINDOW_COUNT and re-check")
        for r in produced:
            merged[(r["period_label"], r["series"])] = r

    if visual_count == 0:
        raise RuntimeError(f"{entity_id}: report {rk} has no data visuals")
    rows = list(merged.values())
    if not rows:
        raise RuntimeError(f"{entity_id}: decoded 0 rows from {visual_count} visual(s)")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"eskom-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

_TRANSFORM_SQL = '''
    SELECT
        period_label,
        CASE WHEN period_ms IS NOT NULL
             THEN epoch_ms(CAST(period_ms AS BIGINT)) END AS period_ts,
        series,
        CAST(value AS DOUBLE)                            AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
      AND period_label IS NOT NULL
      AND series IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_TRANSFORM_SQL.format(dep=s.id))
    for s in DOWNLOAD_SPECS
]
