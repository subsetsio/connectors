"""Hong Kong Census and Statistics Department — web-table connector.

Mechanism: web_table_mdt_csv (the static MDT CSV path).

Per table (tb_code):
  1. GET https://www.censtatd.gov.hk/data/table_{tb_code}_comp.json
     -> theme_id + table_component_list[].{stat_var, stat_pres}
  2. For each component download
     https://www.censtatd.gov.hk/data/MDT_{theme_id}_{tb_code}_{stat_var}_{stat_pres}.csv
     (the literal "%" in stat_pres is rendered "percent" in the filename).
  3. Each CSV is the FULL time series: classification columns vary per table
     (e.g. SEX, AGE), plus a frequency code column, a period column (CCYY for the
     year, optionally Q / M3M / H for sub-annual), obs_value, sd_value.

Raw is written as NDJSON because the column set is heterogeneous across the ~554
tables (and can differ between components of one table). Each row carries every
original CSV column verbatim plus stat_var / stat_pres / value (obs_value cast to
float). Stateless full re-pull every run — the whole corpus is small and the CSVs
have no incremental filter; revisions are picked up for free via overwrite.
"""
import csv
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

from constants import ENTITY_IDS, ASSET_TO_TB, SLUG

COMP_URL = "https://www.censtatd.gov.hk/data/table_{tb}_comp.json"
MDT_URL = "https://www.censtatd.gov.hk/data/MDT_{theme}_{tb}_{sv}_{sp}.csv"


@transient_retry()
def _get(url):
    resp = get(url, timeout=(10.0, 120.0))
    return resp


@transient_retry()
def _get_comp(tb):
    resp = get(COMP_URL.format(tb=tb), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _to_float(raw):
    raw = (raw or "").strip()
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _clean(v):
    """Empty -> None; strip a stray matched pair of surrounding double quotes.
    A few component CSVs deliver classification codes pre-quoted (e.g. SEX as
    `"F"`/`"M"` in table 215-16002), which csv.DictReader preserves verbatim;
    normalize them to the bare code so dimension values don't split."""
    if v is None or v == "":
        return None
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1]
    return v


def _parse_csv(text, sv, sp):
    """Yield one dict per data row, original columns + stat_var/stat_pres/value."""
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        out = {}
        for k, v in row.items():
            if k in ("obs_value", "sd_value") or k is None:
                continue
            out[k] = _clean(v)
        out["stat_var"] = sv
        out["stat_pres"] = sp
        out["value"] = _to_float(row.get("obs_value"))
        out["sd_value"] = _to_float(row.get("sd_value"))
        yield out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    tb = ASSET_TO_TB[node_id]

    comp = _get_comp(tb)
    theme = comp.get("theme_id")
    components = comp.get("table_component_list") or []

    rows = []
    for c in components:
        sv, sp = c.get("stat_var"), c.get("stat_pres")
        if not sv or not sp:
            continue
        url = MDT_URL.format(theme=theme, tb=tb, sv=sv, sp=sp.replace("%", "percent"))
        resp = _get(url)
        if resp.status_code == 200:
            rows.extend(_parse_csv(resp.text, sv, sp))
            continue
        if resp.status_code in (400, 403, 404):
            # Some declared presentations have no static MDT CSV (computed views).
            # Treat as a permanently-missing component for this table and move on.
            print(f"{asset}: component {sv}/{sp} unavailable (HTTP {resp.status_code}) {url}")
            continue
        resp.raise_for_status()

    # Components of one table can carry different classification columns (e.g. one
    # has SEX, another doesn't). Backfill every row to the union of keys so the
    # NDJSON file is internally uniform — otherwise DuckDB's JSON reader infers a
    # schema from an early sample and rejects later rows with extra keys.
    all_keys = set()
    for r in rows:
        all_keys.update(r.keys())
    for r in rows:
        for k in all_keys:
            r.setdefault(k, None)

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE value IS NOT NULL',
    )
    for s in DOWNLOAD_SPECS
]
