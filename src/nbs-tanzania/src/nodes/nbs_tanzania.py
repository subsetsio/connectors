"""NBS Tanzania — SDG indicator time-series (Goal Tracker platform).

Mechanism: goaltracker_sdg. The site is a Next.js SSG app; the entire corpus
lives behind one build-id-stamped `_next/data` URL. The build id changes on
every redeploy, so each run resolves it fresh from the page HTML, then fetches a
single goals JSON (any area/goal pair returns the WHOLE corpus: both areas —
Mainland and Zanzibar — with all goals/targets/indicators and per-indicator
time-series). One ~1.8MB request.

Stateless full re-pull: the corpus is tiny (~7k observation rows), so every run
re-fetches and overwrites. The source exposes no incremental query. Collect
normalised the one corpus into four raw assets; each download node re-derives
its slice from the same corpus fetch:

  - goals       : the 17 SDG goals (universal taxonomy, deduped across areas)
  - targets     : the 169 SDG targets (universal taxonomy, deduped across areas)
  - indicators  : one row per (indicator, area) — id + description
  - values      : long-format observations (indicator x area x year x disaggregation)

The live corpus contains a small number of malformed Mainland indicator records
with no indicator id. Those rows and their observations are skipped because they
cannot be keyed or joined back to the SDG taxonomy.
"""

import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://tanzaniagoaltrack.nbs.go.tz"

GOALS_SCHEMA = pa.schema([
    ("goal_id", pa.int32()),
    ("goal", pa.string()),
])

TARGETS_SCHEMA = pa.schema([
    ("target_id", pa.string()),   # mixed forms in source: 1.1 (float) and 1.A / 17.10 (string)
    ("target", pa.string()),
])

INDICATORS_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("area", pa.string()),
    ("description", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("area", pa.string()),
    ("year", pa.int32()),
    ("value", pa.string()),          # raw; the source mixes str/int/float — transform TRY_CASTs to DOUBLE
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
    """Return the corpus dict: {area: {framework: {indicators, goals, targets, ...}}}."""
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
    data = payload["pageProps"]["data"]
    if not isinstance(data, dict) or not data:
        raise RuntimeError("Goal Tracker corpus payload was empty — buildId or route changed")
    return data


def _disaggregation_label(series: dict) -> str:
    """A stable, canonical string for a series' disaggregation breakdown.

    Sorted 'type=value | type=value ...' so the same breakdown always renders
    identically (part of the values grain)."""
    pairs = series.get("disaggregations") or []
    items = sorted(
        ((str(d.get("type")), str(d.get("value"))) for d in pairs if d.get("type") is not None),
        key=lambda t: (t[0], t[1]),
    )
    return " | ".join(f"{t}={v}" for t, v in items)


def fetch_goals(node_id: str) -> None:
    data = _fetch_corpus()
    seen = {}
    for area in sorted(data.keys()):
        for g in data[area].get("sdg", {}).get("goals", []):
            gid = g.get("Goal Id")
            if gid is None:
                continue
            seen.setdefault(int(gid), g.get("Goal"))
    rows = [{"goal_id": gid, "goal": title} for gid, title in sorted(seen.items())]
    table = pa.Table.from_pylist(rows, schema=GOALS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_targets(node_id: str) -> None:
    data = _fetch_corpus()
    seen = {}
    for area in sorted(data.keys()):
        for t in data[area].get("sdg", {}).get("targets", []):
            tid = t.get("Target id")
            if tid is None:
                continue
            seen.setdefault(str(tid), t.get("Target"))
    rows = [{"target_id": tid, "target": text} for tid, text in sorted(seen.items())]
    table = pa.Table.from_pylist(rows, schema=TARGETS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_indicators(node_id: str) -> None:
    data = _fetch_corpus()
    rows = []
    for area in sorted(data.keys()):
        for ind in data[area].get("sdg", {}).get("indicators", []):
            iid = ind.get("id")
            if iid is None:
                continue
            rows.append({
                "indicator_id": str(iid),
                "area": area,
                "description": ind.get("description"),
            })
    table = pa.Table.from_pylist(rows, schema=INDICATORS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_values(node_id: str) -> None:
    data = _fetch_corpus()
    seen = {}  # (indicator_id, area, year, disaggregation) -> row; keep first non-null value
    for area in sorted(data.keys()):
        for ind in data[area].get("sdg", {}).get("indicators", []):
            iid = ind.get("id")
            if iid is None:
                continue
            iid = str(iid)
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
                    if existing is not None and (existing["value"] is not None or val_str is None):
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
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nbs-tanzania-goals", fn=fetch_goals, kind="download"),
    NodeSpec(id="nbs-tanzania-targets", fn=fetch_targets, kind="download"),
    NodeSpec(id="nbs-tanzania-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="nbs-tanzania-values", fn=fetch_values, kind="download"),
]
