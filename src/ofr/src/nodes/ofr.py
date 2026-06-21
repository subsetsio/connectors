"""OFR (US Office of Financial Research) connector.

Three publishable shapes, all no-auth REST/CSV (stateless full re-pull — the
whole corpus is a handful of dataset requests + one CSV, cheap every run):

* 9 API datasets (STFM: FNYR/MMF/NYPD/REPO/TYLD; HFM: FPF/TFF/SCOOS/FICC) —
  each `GET /series/dataset/?dataset=<code>` returns every series in the dataset
  as `timeseries.aggregation = [[date, value], ...]`. Flattened to long-format
  (mnemonic, date, value) raw; one published table per dataset.
* FSI — single stable bulk CSV (Date + headline index + 8 components), full
  daily history from 2000. Published wide.
* Series catalog — per-series metadata harvested from the same 9 dataset
  endpoints (one row per mnemonic), joinable reference data.

No incremental: the source exposes optional startdate/enddate but the full
corpus is tiny, so we re-pull and overwrite each refresh (revisions free).
"""

import csv
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

from constants import DATASETS, ENTITY_IDS, FSI_CSV_URL


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
@transient_retry()
def _get_json(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_text(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _entity_from_node(node_id):
    """`ofr-repo` -> `REPO`. Recovers the (uppercase) entity id the spec covers."""
    return node_id[len("ofr-"):].upper()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
DATASET_SCHEMA = pa.schema([
    ("mnemonic", pa.string()),
    ("date", pa.string()),       # ISO YYYY-MM-DD as published; cast in transform
    ("value", pa.float64()),     # nullable — holidays / missing observations
])

FSI_COLUMNS = [
    ("Date", "date", pa.string()),
    ("OFR FSI", "ofr_fsi", pa.float64()),
    ("Credit", "credit", pa.float64()),
    ("Equity valuation", "equity_valuation", pa.float64()),
    ("Safe assets", "safe_assets", pa.float64()),
    ("Funding", "funding", pa.float64()),
    ("Volatility", "volatility", pa.float64()),
    ("United States", "united_states", pa.float64()),
    ("Other advanced economies", "other_advanced_economies", pa.float64()),
    ("Emerging markets", "emerging_markets", pa.float64()),
]
FSI_SCHEMA = pa.schema([(clean, typ) for _src, clean, typ in FSI_COLUMNS])

CATALOG_SCHEMA = pa.schema([
    ("mnemonic", pa.string()),
    ("dataset", pa.string()),
    ("monitor", pa.string()),
    ("name", pa.string()),
    ("subtype", pa.string()),
    ("frequency", pa.string()),
    ("unit_type", pa.string()),
    ("unit_name", pa.string()),
    ("start_date", pa.string()),
])


# ---------------------------------------------------------------------------
# Fetch functions
# ---------------------------------------------------------------------------
def fetch_dataset(node_id):
    """One OFR API dataset -> long-format (mnemonic, date, value) raw parquet."""
    asset = node_id
    entity = _entity_from_node(node_id)
    cfg = DATASETS[entity]
    payload = _get_json(f"{cfg['base']}/series/dataset/?dataset={cfg['api_code']}")
    series = payload["timeseries"]

    rows = []
    for mnemonic, body in series.items():
        agg = body.get("timeseries", {}).get("aggregation", []) or []
        for point in agg:
            date, value = point[0], point[1]
            rows.append({
                "mnemonic": mnemonic,
                "date": date,
                "value": float(value) if value is not None else None,
            })

    if not rows:
        raise AssertionError(f"{asset}: dataset returned 0 observations")
    table = pa.Table.from_pylist(rows, schema=DATASET_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_fsi(node_id):
    """OFR Financial Stress Index bulk CSV -> wide raw parquet."""
    asset = node_id
    text = _get_text(FSI_CSV_URL)
    reader = csv.DictReader(io.StringIO(text))

    def _num(v):
        v = (v or "").strip()
        if v == "":
            return None
        return float(v)

    rows = []
    for r in reader:
        rows.append({
            clean: (r.get(src) if clean == "date" else _num(r.get(src)))
            for src, clean, _typ in FSI_COLUMNS
        })

    if not rows:
        raise AssertionError(f"{asset}: FSI CSV parsed to 0 rows")
    table = pa.Table.from_pylist(rows, schema=FSI_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_series_catalog(node_id):
    """Harvest per-series metadata across all 9 datasets -> one row per mnemonic."""
    asset = node_id
    rows = []
    for entity, cfg in DATASETS.items():
        payload = _get_json(f"{cfg['base']}/series/dataset/?dataset={cfg['api_code']}")
        for mnemonic, body in payload["timeseries"].items():
            md = body.get("metadata", {}) or {}
            desc = md.get("description", {}) or {}
            sched = md.get("schedule", {}) or {}
            unit = md.get("unit", {}) or {}
            rows.append({
                "mnemonic": mnemonic,
                "dataset": entity,
                "monitor": cfg["monitor"],
                "name": desc.get("name"),
                "subtype": desc.get("subtype"),
                "frequency": sched.get("observation_frequency"),
                "unit_type": unit.get("type"),
                "unit_name": unit.get("name"),
                "start_date": sched.get("start_date"),
            })

    if not rows:
        raise AssertionError(f"{asset}: series catalog harvested 0 series")
    table = pa.Table.from_pylist(rows, schema=CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------
def _spec_id(entity_id):
    return f"ofr-{entity_id.lower().replace('_', '-')}"


def _fn_for(entity_id):
    if entity_id == "FSI":
        return fetch_fsi
    if entity_id == "ofr-series-catalog":
        return fetch_series_catalog
    return fetch_dataset


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=_fn_for(eid), kind="download")
    for eid in ENTITY_IDS
]

# id helpers for the transforms below
_FSI_ID = _spec_id("FSI")
_CATALOG_ID = _spec_id("ofr-series-catalog")


def _transform_sql(download_id):
    if download_id == _FSI_ID:
        return f'''
            SELECT
                CAST(date AS DATE) AS date,
                ofr_fsi, credit, equity_valuation, safe_assets, funding,
                volatility, united_states, other_advanced_economies, emerging_markets
            FROM "{download_id}"
            WHERE date IS NOT NULL
            ORDER BY date
        '''
    if download_id == _CATALOG_ID:
        return f'''
            SELECT
                mnemonic, dataset, monitor, name, subtype,
                frequency, unit_type, unit_name,
                TRY_CAST(NULLIF(start_date, '') AS DATE) AS start_date
            FROM "{download_id}"
            WHERE mnemonic IS NOT NULL
        '''
    # long-format dataset table
    return f'''
        SELECT
            CAST(date AS DATE) AS date,
            mnemonic,
            CAST(value AS DOUBLE) AS value
        FROM "{download_id}"
        WHERE value IS NOT NULL AND date IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
