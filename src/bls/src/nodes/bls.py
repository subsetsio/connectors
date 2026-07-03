"""BLS connector — bulk flat-file time series, one Delta table per survey database.

Mechanism: `bulk_flatfiles` (research's chosen surface). Every survey database under
https://download.bls.gov/pub/time.series/<survey>/ exposes its entire corpus as a
handful of stable-URL, tab-delimited flat files — no auth, no pagination, no
per-series request. Per survey we:

  1. parse the HTML directory listing to find every `<survey>.data.N.*` observation
     file (long-format rows: series_id, year, period, value, footnote_codes),
  2. stream each file and write the parsed rows to a single parquet raw asset.

The published subset per survey is the observation table: series_id, year, period,
a derived `date`, and the numeric value.

Fetch shape: stateless full re-pull (shape 1). The flat files carry no incremental
delta filter — each refresh re-fetches the whole corpus and overwrites the asset, so
revisions and late corrections are picked up for free. CES (`ce`, ~772MB) and CPI
(`cu`, ~137MB) are the large ones; everything is streamed batch-by-batch so memory
stays bounded regardless of file size.

CRITICAL AUTH QUIRK: download.bls.gov returns HTTP 403 to the default/empty
User-Agent. A descriptive User-Agent (incl. a contact email, ASCII only) is mandatory
on every request — set once via configure_http() at the top of the fetch fn.
"""
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    configure_http,
    raw_parquet_writer,
    transient_retry,
)

# The entity union — the rank-active BLS survey databases (work/entity_union.json).
from constants import ENTITY_IDS

# download.bls.gov 403s the default UA; a descriptive UA (with contact) is required.
_USER_AGENT = "subsets.io data connector (contact: nathansnellaert@gmail.com)"
_BASE = "https://download.bls.gov/pub/time.series"

# Observation files share a stable 5-column tab-delimited schema across every survey.
SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("year", pa.int32()),
    ("period", pa.string()),
    ("value", pa.string()),          # kept raw ("-" sentinels exist); TRY_CAST in SQL
    ("footnote_codes", pa.string()),
])

_BATCH_ROWS = 250_000


@transient_retry()
def _list_data_files(survey: str) -> list[str]:
    """Parse the survey's HTML directory listing into absolute data-file URLs."""
    resp = get_client().get(f"{_BASE}/{survey}/", timeout=(10.0, 120.0))
    resp.raise_for_status()
    hrefs = re.findall(r'<A HREF="([^"]+)">', resp.text, flags=re.IGNORECASE)
    pat = re.compile(rf"/{re.escape(survey)}\.data\.[^/\"]+$")
    files = sorted({h for h in hrefs if pat.search(h)})
    if not files:
        raise AssertionError(f"{survey}: no .data. files found in directory listing")
    return [f"https://download.bls.gov{h}" if h.startswith("/") else h for h in files]


@transient_retry()
def _stream_file_to_batches(url: str) -> list[pa.Table]:
    """Stream one tab-delimited data file, returning parsed parquet batches.

    Streaming (not full-body read) keeps memory bounded for the 348MB CES file.
    Batches are only returned after the full stream completes, so a mid-stream
    transient failure is retried cleanly without committing partial rows.
    """
    batches: list[pa.Table] = []
    sid: list[str] = []
    yr: list = []
    per: list[str] = []
    val: list[str] = []
    fnt: list[str] = []

    def flush() -> None:
        if not sid:
            return
        batches.append(pa.table({
            "series_id": pa.array(sid, pa.string()),
            "year": pa.array(yr, pa.int32()),
            "period": pa.array(per, pa.string()),
            "value": pa.array(val, pa.string()),
            "footnote_codes": pa.array(fnt, pa.string()),
        }, schema=SCHEMA))
        sid.clear(); yr.clear(); per.clear(); val.clear(); fnt.clear()

    with get_client().stream("GET", url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        first = True
        for line in resp.iter_lines():
            cols = line.split("\t")
            if len(cols) < 5:
                continue
            s = cols[0].strip()
            if first:
                first = False
                if s == "series_id":          # header row
                    continue
            year_raw = cols[1].strip()
            if not year_raw.isdigit():         # defensive: skip any malformed line
                continue
            sid.append(s)
            yr.append(int(year_raw))
            per.append(cols[2].strip())
            val.append(cols[3].strip())
            fnt.append(cols[4].strip())
            if len(sid) >= _BATCH_ROWS:
                flush()
    flush()
    return batches


def fetch_one(node_id: str) -> None:
    """Fetch every observation file for one survey database into a single parquet asset."""
    configure_http(headers={"User-Agent": _USER_AGENT})
    asset = node_id                       # the spec id IS the asset name
    survey = node_id[len("bls-"):]        # recover the survey abbreviation

    urls = _list_data_files(survey)
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for url in urls:
            for batch in _stream_file_to_batches(url):
                writer.write_table(batch)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"bls-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# Thin parse-and-type pass: cast value, derive a representative `date` from the BLS
# period code (M01-M12 monthly; Q01-Q04 quarter start; S01/S02 semiannual; annual
# aggregates M13/Q05/S03/A01 land on Jan 1 — `period` disambiguates them). Rows whose
# value isn't numeric ("-" sentinels) are dropped.
#
# Dedup on the (series_id, year, period) grain: BLS ships a redundant `<survey>.data.0.Current`
# convenience file alongside the canonical per-item/area data files, so current-year (and, for
# single-year surveys, every) observation is delivered twice — byte-for-byte identical rows
# (verified: 0 value conflicts among duplicate keys across cu/la/ce). The raw faithfully captures
# all source files; we collapse the duplicates here so each published series has one row per period.
def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            series_id,
            year,
            period,
            CASE
                WHEN period BETWEEN 'M01' AND 'M12'
                    THEN make_date(year, CAST(substr(period, 2, 2) AS INTEGER), 1)
                WHEN period IN ('Q01', 'Q02', 'Q03', 'Q04')
                    THEN make_date(year, (CAST(substr(period, 2, 2) AS INTEGER) - 1) * 3 + 1, 1)
                WHEN period = 'S01' THEN make_date(year, 1, 1)
                WHEN period = 'S02' THEN make_date(year, 7, 1)
                ELSE make_date(year, 1, 1)
            END AS date,
            TRY_CAST(value AS DOUBLE) AS value,
            footnote_codes
        FROM "{download_id}"
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY series_id, year, period ORDER BY footnote_codes) = 1
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_transform_sql(s.id),
                key=("series_id", "year", "period"), temporal="date")
    for s in DOWNLOAD_SPECS
]
