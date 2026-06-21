"""Bundesbank connector — German central bank macro/financial time series.

Source: Deutsche Bundesbank SDMX 2.1 REST API
(https://api.statistiken.bundesbank.de/rest). The corpus is ~85 *dataflows*
(BBDA1 external trade, BBBK1 banks BSI, BBNZ1 national accounts, ...), each a
collection of many individual time series sharing a DSD.

Fetch strategy — stateless full re-pull (shape 1). One GET per dataflow with
`Accept: application/vnd.sdmx.data+csv` returns the *entire* dataflow as long
SDMX-CSV: one row per observation, with the series key (BBK_ID), human title
(BBK_TITLE), TIME_PERIOD, OBS_VALUE, unit and frequency columns that are present
in every dataflow. There is no source-side change feed, so each refresh re-pulls
each dataflow in full and overwrites — revisions and late corrections are picked
up for free. The dimension columns differ per dataflow; we keep only the common
cross-dataflow columns so one generic transform publishes every dataflow.

Memory: a few dataflows are large (BBBK1 ~2.3GB / 5.6M obs, BBSIS ~720MB), so the
CSV is streamed line-by-line and written to parquet in bounded row-group batches
via `raw_parquet_writer` — never buffered whole in RAM.

One dataflow needs special handling: BBKRT (the real-time/vintage database, 11
dimensions including release year/month/day) is too large to materialize in a
single request (HTTP 413). It is fetched one vintage *release year* at a time —
each year written as its own batch file `bundesbank-bbkrt-<year>.parquet`. The
transform's dep view globs `bundesbank-bbkrt-*` and unions every year, so the
published table is identical in shape to every other dataflow's.
"""
import csv
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

API = "https://api.statistiken.bundesbank.de/rest/data"
CODELIST = "https://api.statistiken.bundesbank.de/rest/metadata/codelist/BBK"
# Long SDMX-CSV (one row per observation). The default ?format=csv is the wide
# Bundesbank matrix; the SDMX media type yields the tidy long shape we want.
SDMX_CSV = "application/vnd.sdmx.data+csv;version=1.0.0"
_SDMX_NS = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}

# The entity union — one dataflow id per published subset. Copied from
# data/sources/bundesbank/work/entity_union.json (85 dataflows).
from constants import ENTITY_IDS

# Columns kept from the long SDMX-CSV — present in every dataflow. Dimension
# columns vary per dataflow and are intentionally dropped; BBK_ID already encodes
# the full dotted dimension key and BBK_TITLE gives the human label.
SCHEMA = pa.schema([
    ("dataflow", pa.string()),
    ("series_id", pa.string()),
    ("title", pa.string()),
    ("time_period", pa.string()),
    ("time_format", pa.string()),
    ("unit", pa.string()),
    ("unit_mult", pa.string()),
    ("decimals", pa.string()),
    ("value", pa.float64()),
])

# source CSV column -> SCHEMA field
_KEEP = {
    "DATAFLOW": "dataflow",
    "BBK_ID": "series_id",
    "BBK_TITLE": "title",
    "TIME_PERIOD": "time_period",
    "TIME_FORMAT": "time_format",
    "BBK_UNIT": "unit",
    "BBK_UNIT_MULT": "unit_mult",
    "BBK_DECIMALS": "decimals",
    "OBS_VALUE": "value",
}

BATCH_ROWS = 250_000

# BBKRT (real-time/vintage DB) is fetched one release year at a time. Its DSD has
# 11 dimensions with the release year at position 9 (1-based); a key that pins
# only that dimension is 8 empty fields, the year, then 2 empty fields.
_BBKRT = "BBKRT"
_BBKRT_NDIMS = 11
_BBKRT_YEAR_POS = 9  # 1-based dimension position of BBK_RTD_REL_YEAR
_BBKRT_YEAR_CODELIST = "CL_BBK_RTD_REL_YEAR"


def _to_float(raw):
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


def _batch(rows):
    """Turn a list of {source_col: value} dicts into a RecordBatch under SCHEMA."""
    cols = {name: [] for name in SCHEMA.names}
    for r in rows:
        cols["dataflow"].append(r.get("DATAFLOW"))
        cols["series_id"].append(r.get("BBK_ID"))
        cols["title"].append(r.get("BBK_TITLE"))
        cols["time_period"].append(r.get("TIME_PERIOD"))
        cols["time_format"].append(r.get("TIME_FORMAT"))
        cols["unit"].append(r.get("BBK_UNIT"))
        cols["unit_mult"].append(r.get("BBK_UNIT_MULT"))
        cols["decimals"].append(r.get("BBK_DECIMALS"))
        cols["value"].append(_to_float(r.get("OBS_VALUE")))
    return pa.record_batch(
        [pa.array(cols[name], type=SCHEMA.field(name).type) for name in SCHEMA.names],
        schema=SCHEMA,
    )


def _stream_csv_into(url: str, writer) -> int:
    """Stream one long-SDMX-CSV request and write it to `writer` in row-group
    batches. Returns the number of observation rows written.

    Caller owns retry/atomicity: this helper assumes a fresh (truncated) target,
    so the retried unit that calls it must reopen the writer on retry.
    """
    client = get_client()
    written = 0
    # (connect, read) — read timeout is per-chunk, generous for big dataflows.
    with client.stream("GET", url, headers={"Accept": SDMX_CSV},
                       timeout=(15.0, 300.0)) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines(), delimiter=";")
        try:
            header = next(reader)
        except StopIteration:
            return 0
        if header and header[0].startswith("﻿"):
            header[0] = header[0].lstrip("﻿")
        keep_idx = {src: i for i, src in enumerate(header) if src in _KEEP}

        rows = []
        for fields in reader:
            if not fields:
                continue
            rows.append({src: (fields[i] if i < len(fields) else None)
                         for src, i in keep_idx.items()})
            if len(rows) >= BATCH_ROWS:
                rb = _batch(rows)
                writer.write_batch(rb)
                written += rb.num_rows
                rows = []
        if rows:
            rb = _batch(rows)
            writer.write_batch(rb)
            written += rb.num_rows
    return written


@transient_retry()
def _fetch_dataflow(asset: str, flow: str) -> int:
    """Fetch a whole dataflow into a single parquet asset. The writer is opened
    inside the retried body, so a transient mid-stream failure reopens (and
    truncates) the asset and re-streams — no partial/duplicate rows survive."""
    with raw_parquet_writer(asset, SCHEMA) as writer:
        return _stream_csv_into(f"{API}/{flow}", writer)


@transient_retry()
def _fetch_bbkrt_year(asset_year: str, flow: str, year: str) -> int:
    """Fetch one BBKRT release year into its own batch asset. Same reopen-on-retry
    atomicity as a whole dataflow, scoped to the year so a blip re-pulls only that
    year. The transform globs all year files back together."""
    parts = [""] * _BBKRT_NDIMS
    parts[_BBKRT_YEAR_POS - 1] = year
    key = ".".join(parts)
    with raw_parquet_writer(asset_year, SCHEMA) as writer:
        return _stream_csv_into(f"{API}/{flow}/{key}", writer)


@transient_retry()
def _discover_years(codelist_id: str) -> list[str]:
    resp = get(f"{CODELIST}/{codelist_id}", headers={"Accept": "application/xml"},
               timeout=(15.0, 120.0))
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    years = [c.get("id") for c in root.iterfind(".//s:Code", _SDMX_NS) if c.get("id")]
    if not years:
        raise AssertionError(f"{codelist_id}: no codes discovered")
    return years


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = node_id[len("bundesbank-"):].upper()
    if flow == _BBKRT:
        for year in _discover_years(_BBKRT_YEAR_CODELIST):
            _fetch_bbkrt_year(f"{asset}-{year}", flow, year)  # one batch per year
    else:
        _fetch_dataflow(asset, flow)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bundesbank-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per dataflow: a long time-series table keyed by
# (series_id, date). The period parser maps every SDMX TIME_PERIOD shape — annual
# YYYY, monthly YYYY-MM, quarterly YYYY-Qn, semiannual YYYY-Sn, weekly YYYY-Wnn,
# daily YYYY-MM-DD — to the period-start DATE. Rows with a null value are dropped.
def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            CASE
                WHEN regexp_matches(time_period, '^\\d{{4}}$')
                    THEN make_date(CAST(time_period AS INT), 1, 1)
                WHEN regexp_matches(time_period, '^\\d{{4}}-\\d{{2}}$')
                    THEN make_date(
                        CAST(time_period[1:4] AS INT),
                        CAST(time_period[6:7] AS INT), 1)
                WHEN regexp_matches(time_period, '^\\d{{4}}-\\d{{2}}-\\d{{2}}$')
                    THEN CAST(time_period AS DATE)
                WHEN regexp_matches(time_period, '^\\d{{4}}-Q[1-4]$')
                    THEN make_date(
                        CAST(time_period[1:4] AS INT),
                        (CAST(time_period[7:7] AS INT) - 1) * 3 + 1, 1)
                WHEN regexp_matches(time_period, '^\\d{{4}}-S[1-2]$')
                    THEN make_date(
                        CAST(time_period[1:4] AS INT),
                        (CAST(time_period[7:7] AS INT) - 1) * 6 + 1, 1)
                WHEN regexp_matches(time_period, '^\\d{{4}}-W\\d{{2}}$')
                    THEN make_date(CAST(time_period[1:4] AS INT), 1, 1)
                        + ((CAST(time_period[7:8] AS INT) - 1) * 7)
                ELSE NULL
            END AS date,
            time_period,
            time_format AS frequency,
            series_id,
            title,
            unit,
            value
        FROM "{download_id}"
        WHERE value IS NOT NULL
          AND time_period IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
