"""World Bank connector — Indicators API (https://api.worldbank.org/v2).

Three subsets, all sourced from the v2 JSON REST API (every response is a
two-element array [pagination_meta, data]; transport + parse helpers live in
src/utils.py):

- countries   — country/aggregate reference table. Small, stateless full re-pull.
- indicators  — ~29.5k indicator metadata records. Small, stateless full re-pull.
- values      — long-format observations (indicator x country x year). The full
                corpus is far too large for one run, so it is a supervisor-bounded
                firehose: walk the indicator universe in id-sorted order, write one
                parquet batch per chunk, and resume from a watermark = the last
                indicator id completed. The data API exposes no modified-since
                filter, so values are re-derived by sweeping the indicator catalog.
"""
import os

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet, load_state, save_state
from utils import (
    _IndicatorUnavailable,
    _fetch_all_pages,
    _nested,
    _to_float,
    _indicator_rows,
)

# v2: the watermark is now scoped to RUN_ID. Raw is run-scoped
# (<connector>/runs/<run_id>/raw/...) while state persists across runs, so a
# watermark carried across separate refreshes would leave the sweep "drained"
# forever — fetching nothing and starving the transform of raw. Keying state on
# the current RUN_ID makes every new run re-sweep the full corpus from scratch,
# while still resuming across the supervisor's chained jobs *within* one run
# (they share RUN_ID and the run-scoped raw dir).
STATE_VERSION = 2

# How many indicators accumulate into one parquet batch file — tuned so each batch
# lands at a moderate size. There is no per-run indicator/time cap: the loop sweeps
# the whole indicator universe and the supervisor interrupts the node (→ pending →
# continuation) if the run nears its CI wall-clock; per-batch raw+state writes make
# that interrupt safe to resume.
INDICATORS_PER_BATCH = 50

# ---------------------------------------------------------------------------
# countries
# ---------------------------------------------------------------------------
_COUNTRY_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("iso2_code", pa.string()),
    ("name", pa.string()),
    ("region_id", pa.string()),
    ("region_value", pa.string()),
    ("adminregion_id", pa.string()),
    ("adminregion_value", pa.string()),
    ("income_level_id", pa.string()),
    ("income_level_value", pa.string()),
    ("lending_type_id", pa.string()),
    ("lending_type_value", pa.string()),
    ("capital_city", pa.string()),
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
])


def fetch_countries(node_id: str) -> None:
    asset = node_id
    records = _fetch_all_pages("country", {}, per_page=400)
    rows = []
    for r in records:
        rows.append({
            "id": r.get("id"),
            "iso2_code": r.get("iso2Code"),
            "name": (r.get("name") or "").strip(),
            "region_id": _nested(r, "region", "id"),
            "region_value": _nested(r, "region", "value"),
            "adminregion_id": _nested(r, "adminregion", "id"),
            "adminregion_value": _nested(r, "adminregion", "value"),
            "income_level_id": _nested(r, "incomeLevel", "id"),
            "income_level_value": _nested(r, "incomeLevel", "value"),
            "lending_type_id": _nested(r, "lendingType", "id"),
            "lending_type_value": _nested(r, "lendingType", "value"),
            "capital_city": (r.get("capitalCity") or "").strip(),
            "longitude": _to_float(r.get("longitude")),
            "latitude": _to_float(r.get("latitude")),
        })
    table = pa.Table.from_pylist(rows, schema=_COUNTRY_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# indicators
# ---------------------------------------------------------------------------
_INDICATOR_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("unit", pa.string()),
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_note", pa.string()),
    ("source_organization", pa.string()),
    ("topic_ids", pa.string()),
    ("topic_names", pa.string()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    rows = _indicator_rows()
    table = pa.Table.from_pylist(rows, schema=_INDICATOR_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# values (firehose)
# ---------------------------------------------------------------------------
_VALUE_SCHEMA = pa.schema([
    ("indicator_code", pa.string()),
    ("indicator_name", pa.string()),
    ("source_id", pa.string()),
    ("country_id", pa.string()),
    ("country_iso3", pa.string()),
    ("country_name", pa.string()),
    ("date", pa.string()),
    ("value", pa.float64()),
    ("unit", pa.string()),
    ("obs_status", pa.string()),
])


def _fetch_indicator_observations(indicator_id: str, source_id: str):
    """Long-format observations for one indicator across all countries/years."""
    params = {}
    if source_id:
        params["source"] = source_id
    try:
        records = _fetch_all_pages(
            f"country/all/indicator/{indicator_id}", params, per_page=20000
        )
    except _IndicatorUnavailable:
        # Deleted/archived/non-queryable indicator (200 + message envelope).
        return []
    except httpx.HTTPStatusError as exc:
        # A 400/404 that survives the full retry budget means this particular
        # indicator/source pair is not queryable via the data endpoint (a known
        # quirk across the ~29.5k-indicator universe). Skip it rather than sink
        # the entire values sweep on one bad entry.
        if exc.response.status_code in (400, 404):
            return []
        raise
    out = []
    for r in records:
        out.append({
            "indicator_code": _nested(r, "indicator", "id") or indicator_id,
            "indicator_name": _nested(r, "indicator", "value"),
            "source_id": source_id,
            "country_id": _nested(r, "country", "id"),
            "country_iso3": (r.get("countryiso3code") or "").strip(),
            "country_name": _nested(r, "country", "value"),
            "date": (r.get("date") or "").strip(),
            "value": _to_float(r.get("value")),
            "unit": (r.get("unit") or "").strip(),
            "obs_status": (r.get("obs_status") or "").strip(),
        })
    return out


def fetch_values(node_id: str) -> None:
    state_key = node_id  # "world-bank-values"
    state = load_state(state_key)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "watermark": ""}
    watermark = state.get("watermark", "")

    # Discover the full indicator universe (id-sorted) every run. The list is
    # cheap (~2 pages) and being recomputed makes new indicators show up at the
    # tail automatically.
    catalog = sorted(
        ((r["id"], r["source_id"]) for r in _indicator_rows() if r.get("id")),
        key=lambda t: t[0],
    )
    total = len(catalog)
    start_idx = next((i for i, (iid, _) in enumerate(catalog) if iid > watermark), total)

    idx = start_idx
    while idx < total:
        chunk = catalog[idx:idx + INDICATORS_PER_BATCH]
        batch_rows = []
        for indicator_id, source_id in chunk:
            batch_rows.extend(_fetch_indicator_observations(indicator_id, source_id))

        batch_key = f"{idx:06d}-{idx + len(chunk) - 1:06d}"
        if batch_rows:
            table = pa.Table.from_pylist(batch_rows, schema=_VALUE_SCHEMA)
            save_raw_parquet(table, f"{node_id}-{batch_key}")  # write raw FIRST

        # Advance watermark to the last indicator id in this chunk, then persist.
        state = {"schema_version": STATE_VERSION, "watermark": chunk[-1][0]}
        save_state(state_key, state)

        idx += len(chunk)


# ---------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="world-bank-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="world-bank-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="world-bank-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-bank-countries-transform",
        deps=["world-bank-countries"],
        sql='''
            SELECT
                id                  AS country_code,
                iso2_code,
                name,
                region_id,
                NULLIF(region_value, '')        AS region,
                NULLIF(income_level_value, '')  AS income_level,
                NULLIF(lending_type_value, '')  AS lending_type,
                NULLIF(capital_city, '')        AS capital_city,
                longitude,
                latitude
            FROM "world-bank-countries"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="world-bank-indicators-transform",
        deps=["world-bank-indicators"],
        sql='''
            SELECT
                id                          AS indicator_code,
                name,
                NULLIF(unit, '')            AS unit,
                source_id,
                NULLIF(source_name, '')     AS source_name,
                NULLIF(source_note, '')     AS definition,
                NULLIF(source_organization, '') AS source_organization,
                NULLIF(topic_names, '')     AS topics
            FROM "world-bank-indicators"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="world-bank-values-transform",
        deps=["world-bank-values"],
        sql='''
            SELECT
                indicator_code,
                indicator_name,
                source_id,
                country_id,
                NULLIF(country_iso3, '')    AS country_iso3,
                country_name,
                TRY_CAST(date AS INTEGER)   AS year,
                date                        AS period,
                CAST(value AS DOUBLE)       AS value,
                NULLIF(obs_status, '')      AS obs_status
            FROM (
                SELECT *,
                    row_number() OVER (
                        PARTITION BY indicator_code, country_id, date
                        ORDER BY value DESC NULLS LAST
                    ) AS _rn
                FROM "world-bank-values"
                WHERE value IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
