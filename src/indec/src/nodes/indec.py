"""INDEC (Instituto Nacional de Estadistica y Censos, Argentina).

INDEC's statistical output is disseminated through Argentina's national
time-series platform ("Series de Tiempo", apis.datos.gob.ar). INDEC content
lives inside the SSPM catalog and is isolated by the exact dataset source label
"Instituto Nacional de Estadistica y Censos (INDEC)" (~9,500 series spanning
prices/IPC, national accounts/EMAE, trade/ICA, labour, demographics, industry).

Mechanism note: research's chosen mechanism was the per-catalog *bulk dump*
(/series/api/dump/sspm/...). That path is dead from outside the platform — the
dump endpoint 302-redirects to a presigned object URL whose SigV4 signature is
bound to an internal host/path, so it returns 403 SignatureDoesNotMatch for any
external client (verified with both httpx and requests, clean redirect-follow).
We therefore use the other verified mechanism from research, `series_rest`:
  - /search/  enumerates INDEC series + metadata (paginated, count=9467).
  - /series/  returns (date,value) streams; multiple ids per call map
    positionally to the data columns (data row = [date, v1, v2, ...]).

This is a homogeneous indicator source, so it publishes two subsets:
  - indec-indec-series : the series catalog (one row per series; reference)
  - indec-indec-values : long-format observations (series_id, date, value)

Stateless full re-pull each run: the whole corpus re-fetches in a few minutes,
so revisions/late corrections are picked up for free (no watermark/cursor).
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    save_raw_parquet,
    transient_retry,
)

SEARCH_URL = "https://apis.datos.gob.ar/series/api/search/"
SERIES_URL = "https://apis.datos.gob.ar/series/api/series/"
# Exact dataset.source label that isolates INDEC inside the mixed SSPM catalog.
INDEC_SOURCE = "Instituto Nacional de Estadística y Censos (INDEC)"

# Page sizes. /search caps at 1000 series/page; /series caps at 1000 periods/page.
SEARCH_PAGE = 1000
SERIES_PERIODS = 1000
# Series ids per /series call. Comfortably under URL limits; batched within a
# single frequency so the wide response stays dense (no cross-frequency nulls).
IDS_PER_CALL = 50

CATALOG_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("frequency", pa.string()),
    ("units", pa.string()),
    ("time_index_start", pa.string()),
    ("time_index_end", pa.string()),
    ("dataset_title", pa.string()),
    ("dataset_source", pa.string()),
    ("dataset_theme", pa.string()),
    ("dataset_publisher", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("date", pa.string()),     # ISO YYYY-MM-DD; transform CASTs to DATE
    ("value", pa.float64()),
])


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _iter_indec_series():
    """Yield each INDEC series record ({'field': ..., 'dataset': ...}) from
    the /search catalog, paginating to full coverage."""
    start = 0
    total = None
    while True:
        d = _get_json(SEARCH_URL, {
            "dataset_source": INDEC_SOURCE,
            "limit": SEARCH_PAGE,
            "start": start,
        })
        if total is None:
            total = d["count"]
        rows = d.get("data") or []
        if not rows:
            break
        for rec in rows:
            yield rec
        start += SEARCH_PAGE
        if start >= total:
            break


# ---------------------------------------------------------------------------
# indec-indec-series — the series catalog (reference)
# ---------------------------------------------------------------------------
def fetch_series_catalog(node_id: str) -> None:
    asset = node_id
    rows = []
    for rec in _iter_indec_series():
        f = rec.get("field") or {}
        ds = rec.get("dataset") or {}
        pub = ds.get("publisher") or {}
        rows.append({
            "series_id": f.get("id"),
            "title": f.get("title"),
            "description": f.get("description"),
            "frequency": f.get("frequency"),
            "units": f.get("units"),
            "time_index_start": f.get("time_index_start"),
            "time_index_end": f.get("time_index_end"),
            "dataset_title": ds.get("title"),
            "dataset_source": ds.get("source"),
            "dataset_theme": ds.get("theme"),
            "dataset_publisher": pub.get("name") if isinstance(pub, dict) else None,
        })
    table = pa.Table.from_pylist(rows, schema=CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# indec-indec-values — long-format observations
# ---------------------------------------------------------------------------
def _emit_batch(writer, ids: list[str]) -> None:
    """Fetch every (date,value) for a batch of series ids and stream them as
    long-format record batches. On a 400 (a series id the catalog listed but
    /series rejects), bisect to isolate and skip only the offending id."""
    start = 0
    while True:
        try:
            d = _get_json(SERIES_URL, {
                "ids": ",".join(ids),
                "format": "json",
                "limit": SERIES_PERIODS,
                "start": start,
            })
        except httpx.HTTPStatusError as e:
            if e.response is not None and e.response.status_code == 400:
                if len(ids) > 1:
                    mid = len(ids) // 2
                    _emit_batch(writer, ids[:mid])
                    _emit_batch(writer, ids[mid:])
                    return
                print(f"  skipping series rejected by /series: {ids[0]}")
                return
            raise

        data = d.get("data") or []
        if not data:
            break
        count = d["count"]

        sids: list[str] = []
        dates: list[str] = []
        vals: list[float] = []
        for row in data:
            date = row[0]
            for k, sid in enumerate(ids):
                v = row[k + 1]
                if v is not None:
                    sids.append(sid)
                    dates.append(date)
                    vals.append(float(v))
        if sids:
            writer.write_batch(pa.record_batch(
                {
                    "series_id": pa.array(sids, pa.string()),
                    "date": pa.array(dates, pa.string()),
                    "value": pa.array(vals, pa.float64()),
                },
                schema=VALUES_SCHEMA,
            ))

        start += SERIES_PERIODS
        if start >= count:
            break


def fetch_values(node_id: str) -> None:
    asset = node_id
    # Group ids by frequency so each /series batch is one frequency and the
    # wide response stays dense (avoids huge sparse cross-frequency tables).
    by_freq: dict[str, list[str]] = {}
    for rec in _iter_indec_series():
        f = rec.get("field") or {}
        sid = f.get("id")
        if not sid:
            continue
        by_freq.setdefault(f.get("frequency") or "unknown", []).append(sid)

    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for ids in by_freq.values():
            for i in range(0, len(ids), IDS_PER_CALL):
                _emit_batch(writer, ids[i:i + IDS_PER_CALL])


DOWNLOAD_SPECS = [
    NodeSpec(id="indec-indec-series", fn=fetch_series_catalog, kind="download"),
    NodeSpec(id="indec-indec-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="indec-indec-series-transform",
        deps=["indec-indec-series"],
        sql='''
            SELECT
                series_id,
                title,
                description,
                frequency,
                units,
                CAST(time_index_start AS DATE) AS time_index_start,
                CAST(time_index_end   AS DATE) AS time_index_end,
                dataset_title,
                dataset_source,
                dataset_theme,
                dataset_publisher
            FROM "indec-indec-series"
            WHERE series_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="indec-indec-values-transform",
        deps=["indec-indec-values"],
        sql='''
            SELECT DISTINCT
                series_id,
                CAST(date AS DATE)    AS date,
                CAST(value AS DOUBLE) AS value
            FROM "indec-indec-values"
            WHERE value IS NOT NULL
              AND series_id IS NOT NULL
        ''',
    ),
]
